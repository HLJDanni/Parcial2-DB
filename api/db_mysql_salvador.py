import os

# Configuración de MySQL para El Salvador
MYSQL_USER_SALVADOR = os.getenv("MYSQL_USER_SALVADOR", "root")
MYSQL_PASSWORD_SALVADOR = os.getenv("MYSQL_PASSWORD_SALVADOR", "root")
MYSQL_HOST_SALVADOR = os.getenv("DB_MYSQL_SALVADOR_HOST", "mysql_salvador")
MYSQL_DATABASE_SALVADOR = os.getenv("MYSQL_DATABASE_SALVADOR", "sucursal_elsalvador")


# Conexión para El Salvador
mysql_config_salvador = {
    'host': MYSQL_HOST_SALVADOR,
    'user': MYSQL_USER_SALVADOR,
    'password': MYSQL_PASSWORD_SALVADOR,
    'database': MYSQL_DATABASE_SALVADOR
}