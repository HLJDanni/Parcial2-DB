import os

# Configuración de MySQL para México
MYSQL_USER_MEXICO = os.getenv("MYSQL_USER_MEXICO", "root")
MYSQL_PASSWORD_MEXICO = os.getenv("MYSQL_PASSWORD_MEXICO", "root")
MYSQL_HOST_MEXICO = os.getenv("DB_MYSQL_MEXICO_HOST", "mysql-mexico")
MYSQL_DATABASE_MEXICO = os.getenv("MYSQL_DATABASE_MEXICO", "sucursal_mexico")


# Conexión para México
mysql_config_mexico = {
    'host': MYSQL_HOST_MEXICO,
    'user': MYSQL_USER_MEXICO,
    'password': MYSQL_PASSWORD_MEXICO,
    'database': MYSQL_DATABASE_MEXICO
}


