import os
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
# Each Flask web application contains a secret key which used to sign session cookies for protection against cookie data tampering.
SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode, that will refresh the page when you make changes.
DEBUG = True

# todo:DATABASE CONNECTION
connection_url_mysql = URL.create(
    'mysql+pymysql',
    username='root',
    password='spts@3311',
    host='10.0.0.9',
    port=3306,
    database='sooperwizer'
)

connection_url_postgres = URL.create(
    'postgresql+psycopg2',
    username='postgres',
    password='spts@3311',
    host='10.0.0.9',
    port=5432,
    database='postgres'
)

SQLALCHEMY_DATABASE_URI = connection_url_postgres
# SQLALCHEMY_BINDS = {
#     'connection_url_mysql':        connection_url_mysql
# }

engine_mysql = create_engine(connection_url_mysql)
engine_postgres = create_engine(connection_url_postgres)


SQLALCHEMY_TRACK_MODIFICATIONS = False

print(SQLALCHEMY_DATABASE_URI)
# print(SQLALCHEMY_BINDS)
