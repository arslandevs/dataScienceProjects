from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pandas as pd
# import psycopg2
# import os
# import time
# import csv
# import datetime
from sqlalchemy.orm import Session
import csv
from sqlalchemy import Table, Column, Integer, String, MetaData, BIGINT, ForeignKey
from sqlalchemy.types import DateTime
from sqlalchemy.types import Integer, Float, String, JSON, DateTime, BINARY, LargeBinary,Boolean
from pangres import upsert
from sqlalchemy.orm import  relationship
import os
import psycopg2
import numpy as np
import psycopg2.extras as extras
from io import StringIO
import sys
# %load_ext blackcellmagic

try:
  connection_url_mysql = URL.create(
    'mysql+pymysql',
    username='root',
    password='spts@3311',
    host='10.0.0.9',
    port=3306,
    database='sooperwizer'
  )
  engine_mysql = create_engine(connection_url_mysql)
  # engine.connect()
  session_mysql = Session(engine_mysql, future=True)

except Exception as e:
  print(e)

try: 
  connection_url_postgres = URL.create(
    'postgresql+psycopg2',
    username='postgres',
    password='spts@3311',
    host='10.0.0.9',
    port=5432,
    database='postgres'
  )
  engine_postgres = create_engine(connection_url_postgres)
  session_postgres = Session(engine_postgres, future=True)
except Exception as e:
  print(e)
else:
  print('connection successful')


db_mysql='sooperwizer'
def mysqlRowcount(table):
    rowCount=session_mysql.execute(f'select count(*) from {db_mysql}.{table}').all()[0][0]
    # print(rowCount)
    return rowCount

db_postgres='public'
def postgresRowcount(table):
    rowCount=session_postgres.execute(f'select count(*) from {db_postgres}.{table}').all()[0][0]
    # print(rowCount)
    return rowCount


