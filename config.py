import os

SECRET_KEY = 'leandro'

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "admi"
MYSQL_DB = "cadastro"
MYSQL_PORT = 3306
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) \
              + '/uploards'