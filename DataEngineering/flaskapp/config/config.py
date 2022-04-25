from os import path
from sqlalchemy.engine import URL
basedir = path.abspath(path.dirname(__file__))

CONN_URL_MYSQL = URL.create(
  'mysql+pymysql',
  username='root',
  password='spts@3311',
  host='10.0.0.9',
  port=3306,
  database='sooperwizer'
)

CONN_URL_POSTGRESQL = URL.create(
  'postgresql+psycopg2',
  username='postgres',
  password='spts@3311',
  host='10.0.0.9',
  port=5432,
  database='postgres'
)

class Config(object):
  DEBUG=True
  DEVELOPMENT=True
  SECRET_KEY='mysecret'
  FLASK_SECRET='myflasksecret'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_DATABASE_URI=CONN_URL_POSTGRESQL

