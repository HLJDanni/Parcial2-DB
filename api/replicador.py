import oracledb
import mysql.connector
import time
import logging
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('replicador.log'),
        logging.StreamHandler()
    ]
)

class OracleChangeTracker:
    def __init__(self):
        self.last_checks = {
            'clientes': datetime.min,
            'procuradores': datetime.min,
            'abogados': datetime.min,
            'asuntos': datetime.min
        }

    def check_changes(self, oracle_conn):
        changed_tables = []
        try:
            with oracle_conn.cursor() as cursor:
                for table in self.last_checks.keys():
                    cursor.execute(f"""
                        SELECT MAX(LAST_MODIFIED) 
                        FROM {table}
                        WHERE LAST_MODIFIED > TO_DATE(:last_check, 'YYYY-MM-DD HH24:MI:SS')
                    """, [self.last_checks[table].strftime('%Y-%m-%d %H:%M:%S')])

                    result = cursor.fetchone()
                    if result and result[0]:
                        changed_tables.append(table)
                        self.last_checks[table] = result[0]

        except oracledb.Error as e:
            logging.error(f"Error al verificar cambios: {e}")

        return changed_tables

def connect_oracle():
    max_retries = 10
    retry_delay = 10

    for attempt in range(max_retries):
        try:
            connection = oracledb.connect(
                user="app_user",
                password="oracle123",
                dsn="oracle-db/XE"
            )
            logging.info("Conexión a Oracle establecida correctamente")
            return connection
        except oracledb.Error as e:
            logging.error(f"Intento {attempt + 1} de {max_retries} - Error de conexión a Oracle: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (attempt + 1))

    logging.critical("No se pudo establecer conexión con Oracle")
    return None

def connect_mysql(host, db_name, port=3306):
    try:
        connection = mysql.connector.connect(
            user="root",
            password="root",
            host=host,
            port=port,
            database=db_name
        )
        return connection
    except mysql.connector.Error as e:
        logging.error(f"Error de conexión a MySQL en {host}:{port} (DB: {db_name}): {e}")
        return None

def replicate_table(oracle_conn, mysql_conn, table_name, columns, id_column, last_check_date):
    try:
        with oracle_conn.cursor() as cursor_oracle:
            cursor_oracle.execute(f"""
                SELECT {','.join(columns)} 
                FROM {table_name}
                WHERE LAST_MODIFIED > TO_TIMESTAMP(:last_check, 'YYYY-MM-DD HH24:MI:SS')
            """, [last_check_date.strftime('%Y-%m-%d %H:%M:%S')])

            rows = cursor_oracle.fetchall()

            if not rows:
                logging.debug(f"No hay cambios para replicar en {table_name}")
                return

            placeholders = ','.join(['%s'] * len(columns))
            updates = ','.join([f"{col}=VALUES({col})" for col in columns if col != id_column])

            with mysql_conn.cursor() as cursor_mysql:
                try:
                    cursor_mysql.execute(f"SHOW TABLES LIKE '{table_name}'")
                    if not cursor_mysql.fetchone():
                        logging.error(f"La tabla {table_name} no existe en la base de datos destino")
                        return

                    cursor_mysql.execute("SET @DISABLE_TRIGGERS = TRUE")

                    processed_rows = []
                    for row in rows:
                        processed_row = list(row)
                        for i, val in enumerate(row):
                            if hasattr(val, 'read'):  # Es un LOB
                                processed_row[i] = val.read()
                            elif isinstance(val, datetime):
                                processed_row[i] = val.strftime('%Y-%m-%d %H:%M:%S')
                        processed_rows.append(processed_row)

                    cursor_mysql.executemany(f"""
                        INSERT INTO {table_name} ({','.join(columns)})
                        VALUES ({placeholders})
                        ON DUPLICATE KEY UPDATE {updates}
                    """, processed_rows)

                    mysql_conn.commit()
                    logging.info(f"Replicados {len(rows)} registros en {table_name}")
                except mysql.connector.Error as e:
                    mysql_conn.rollback()
                    logging.error(f"Error replicando {table_name}: {e}")
                finally:
                    cursor_mysql.execute("SET @DISABLE_TRIGGERS = FALSE")

    except Exception as e:
        logging.error(f"Error general replicando {table_name}: {e}")

def setup_oracle_triggers(oracle_conn):
    tables_config = {
        'clientes': {'id_column': 'cliente_id'},
        'procuradores': {'id_column': 'procurador_id'},
        'abogados': {'id_column': 'abogado_id'},
        'asuntos': {'id_column': 'expediente_id'}
    }

    try:
        with oracle_conn.cursor() as cursor:
            cursor.execute("""
                BEGIN
                    EXECUTE IMMEDIATE 'CREATE TABLE deleted_records (
                        id NUMBER GENERATED BY DEFAULT AS IDENTITY,
                        table_name VARCHAR2(50),
                        record_id NUMBER,
                        deletion_time TIMESTAMP,
                        PRIMARY KEY (id)
                    )';
                EXCEPTION
                    WHEN OTHERS THEN
                        IF SQLCODE = -955 THEN NULL;
                        ELSE RAISE;
                        END IF;
                END;
            """)

            for table, config in tables_config.items():
                cursor.execute(f"""
                    BEGIN
                        EXECUTE IMMEDIATE 'ALTER TABLE {table} ADD (LAST_MODIFIED TIMESTAMP DEFAULT SYSTIMESTAMP)';
                    EXCEPTION
                        WHEN OTHERS THEN 
                            IF SQLCODE = -1430 THEN NULL;
                            ELSE RAISE;
                            END IF;
                    END;
                """)

                cursor.execute(f"""
                    CREATE OR REPLACE TRIGGER tr_{table}_modified
                    BEFORE INSERT OR UPDATE ON {table}
                    FOR EACH ROW
                    BEGIN
                        :NEW.LAST_MODIFIED := SYSTIMESTAMP;
                    END;
                """)

                cursor.execute(f"""
                    CREATE OR REPLACE TRIGGER tr_{table}_deleted
                    AFTER DELETE ON {table}
                    FOR EACH ROW
                    DECLARE
                        PRAGMA AUTONOMOUS_TRANSACTION;
                    BEGIN
                        INSERT INTO deleted_records 
                        (table_name, record_id, deletion_time)
                        VALUES ('{table}', :OLD.{config['id_column']}, SYSTIMESTAMP);
                        COMMIT;
                    END;
                """)

            oracle_conn.commit()
            logging.info("Triggers y tabla de auditoría configurados correctamente en Oracle")

    except oracledb.Error as e:
        logging.error(f"Error configurando triggers en Oracle: {e}")
        oracle_conn.rollback()

def replicate_data():
    tables_config = {
        'clientes': {
            'columns': ['cliente_id', 'nombre', 'direccion', 'telefono', 'correo', 'LAST_MODIFIED'],
            'id_column': 'cliente_id'
        },
        'procuradores': {
            'columns': ['procurador_id', 'nombre', 'dni', 'telefono', 'correo', 'LAST_MODIFIED'],
            'id_column': 'procurador_id'
        },
        'abogados': {
            'columns': ['abogado_id', 'nombre', 'dni', 'pais', 'correo', 'LAST_MODIFIED'],
            'id_column': 'abogado_id'
        },
        'asuntos': {
            'columns': ['expediente_id', 'cliente_id', 'descripcion', 'estado', 'fecha_inicio', 'fecha_final', 'LAST_MODIFIED'],
            'id_column': 'expediente_id'
        }
    }

    change_tracker = OracleChangeTracker()
    oracle_conn = connect_oracle()
    if oracle_conn:
        setup_oracle_triggers(oracle_conn)
        oracle_conn.close()

    while True:
        start_time = datetime.now()
        try:
            oracle_conn = connect_oracle()
            if not oracle_conn:
                time.sleep(10)
                continue

            mysql_mexico_conn = connect_mysql("mysql-mexico", "sucursal_mexico", 3306)
            mysql_salvador_conn = connect_mysql("mysql-salvador", "sucursal_elsalvador", 3306)

            if not mysql_mexico_conn or not mysql_salvador_conn:
                time.sleep(10)
                continue

            changed_tables = change_tracker.check_changes(oracle_conn)

            if not changed_tables:
                logging.debug("No se detectaron cambios en las tablas")
            else:
                logging.info(f"Tablas con cambios: {', '.join(changed_tables)}")

                for table in changed_tables:
                    last_check = change_tracker.last_checks[table]
                    replicate_table(oracle_conn, mysql_mexico_conn, table,
                                    tables_config[table]['columns'],
                                    tables_config[table]['id_column'],
                                    last_check)

                    replicate_table(oracle_conn, mysql_salvador_conn, table,
                                    tables_config[table]['columns'],
                                    tables_config[table]['id_column'],
                                    last_check)

            logging.info(f"Ciclo completado en {(datetime.now() - start_time).total_seconds():.2f}s")

        except Exception as e:
            logging.error(f"Error en ciclo de replicación: {e}")
        finally:
            if 'oracle_conn' in locals() and oracle_conn:
                oracle_conn.close()
            if 'mysql_mexico_conn' in locals() and mysql_mexico_conn:
                mysql_mexico_conn.close()
            if 'mysql_salvador_conn' in locals() and mysql_salvador_conn:
                mysql_salvador_conn.close()

        time.sleep(5)

if __name__ == "__main__":
    replicate_data()