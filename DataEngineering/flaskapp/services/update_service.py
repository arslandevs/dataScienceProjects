# import json
# from models.machine import db
# from myconfig import engine_mysql

from config.config import CONN_URL_MYSQL, CONN_URL_POSTGRESQL
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from pangres import upsert
import pandas as pd
# import sys
# sys.path.append("..")
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pandas as pd
import psycopg2
import os
import time
import csv
import datetime
from sqlalchemy.orm import Session
import csv
from sqlalchemy import Table, Column, Integer, String, MetaData, BIGINT, ForeignKey
from sqlalchemy.types import DateTime
from sqlalchemy.types import Integer, Float, String, JSON, DateTime, BINARY, LargeBinary,Boolean
from sqlalchemy.orm import  relationship
import os
import psycopg2
import numpy as np
import psycopg2.extras as extras
from io import StringIO
import sys
from tests import mysqlRowcount,postgresRowcount
# %load_ext blackcellmagic

# engine_mysql = create_engine(CONN_URL_MYSQL)
# engine_postgres = create_engine(CONN_URL_POSTGRESQL)
# session_mysql = Session(engine_mysql)

# todo:CONNECTION MYSQL
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
  
else:
  print('connection successful')

# todo:CONNECTION POSTGRES
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


# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
# MY UPDATE LOGIC
def myupdate(db_tablename,df_table,index):
    """
    df_table:dataframe table name
    index: first column of the dataframe to be set as index of dataframe required for upsert function. 
    db_tablename:table names in the database
    e.g:
    myupdate("line",line_table,"LineID")
    """
    if df_table.columns[0]==index:
        df_table.set_index([index], inplace = True, drop = True)

    upsert(con=engine_postgres,
        df=df_table,
        table_name=db_tablename,
        if_row_exists='update',
        dtype=None,
        create_table=False)
# -----------------------------------------------------------------------
#UPDATION
def update_logic():


    piece_wise_scan = session_mysql.execute("select * from piece_wise_scan").all()
    piece_wise_cut_report = session_mysql.execute(
        "select * from piece_wise_cut_report"
    ).all()
    cut_report = session_mysql.execute("select * from cut_report").all()
    cut_job = session_mysql.execute("select * from cut_job").all()
    production_order = session_mysql.execute("select * from production_order").all()
    sale_order = session_mysql.execute("select * from sale_order").all()
    style_template = session_mysql.execute("select * from style_template").all()
    marker = session_mysql.execute("select * from marker").all()

    worker_scan = session_mysql.execute("select * from worker_scan").all()
    line = session_mysql.execute("select * from line").all()
    worker = session_mysql.execute("select * from worker").all()
    machine = session_mysql.execute("select * from machine").all()

    operation = session_mysql.execute("select * from operation").all()
    section = session_mysql.execute("select * from section").all()
    machine_type = session_mysql.execute("select * from machine_type").all()

    scan = session_mysql.execute("select * from scan").all()

    module = session_mysql.execute("select * from module").all()
    userpermission = session_mysql.execute("select * from userpermission").all()

    style_bulletin = session_mysql.execute("select * from style_bulletin")
    tag = session_mysql.execute("select * from tag")
    user = session_mysql.execute("select * from user")



    machine_table = pd.DataFrame(
        machine,
        columns=[
            "MachineID",
            "MachineCode",
            "MachineDescription",
            "MachineImageUrl",
            "MachineThumbnailUrl",
            "MachineTypeID",
            "ActiveWorkerID",
            "LineID",
            "Operations",
            "CreatedAt",
            "UpdatedAt",
            "BoxID",
            "IsMachineDown"
        ],
    )
    machine_table = machine_table.astype(
        {
            "MachineID": "Int64",
            "MachineCode": "string",
            "MachineDescription": "string",
            "MachineImageUrl": "string",
            "MachineThumbnailUrl": "string",
            "MachineTypeID": "Int64",
            "ActiveWorkerID": "Int64",
            "LineID": "Int64",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
            "BoxID": "Int64",
            "IsMachineDown":"bool",
        }
    )
    # machine_table["Operations"] = machine_table["Operations"].to_json()

    piece_wise_scan_table = pd.DataFrame(
        piece_wise_scan,
        columns=[
            "PieceWiseScanningID",
            "ScanID",
            "BundleID",
            "PieceID",
            "OperationID",
            "WorkerID",
            "LineID",
            "MachineID",
            "CreatedAt",
            "UpdatedAt",
        ],
    )
    piece_wise_scan_table = piece_wise_scan_table.astype(
        {
            "PieceWiseScanningID": "Int64",
            "ScanID": "int64",
            "BundleID": "Int64",
            "PieceID": "Int64",
            "OperationID": "Int64",
            "WorkerID": "Int64",
            "LineID": "Int64",
            "MachineID": "Int64",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
        }
    )

    scan_table = pd.DataFrame(
        scan,
        columns=[
            "ScanID",
            "WorkerScanID",
            "BundleID",
            "PieceID",
            "OperationID",
            "WorkerID",
            "LineID",
            "MachineID",
            "ShortAddress",
            "LongAddress",
            "HostIP",
            "CreatedAt",
            "UpdatedAt",
        ],
    )
    scan_table = scan_table.astype(
        {
            "ScanID": "Int64",
            "WorkerScanID": "Int64",
            "BundleID": "Int64",
            "PieceID": "Int64",
            "OperationID": "Int64",
            "WorkerID": "Int64",
            "LineID": "Int64",
            "MachineID": "Int64",
            "ShortAddress": "string",
            "LongAddress": "string",
            "HostIP": "string",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
        }
    )

    worker_scan_table = pd.DataFrame(
        worker_scan,
        columns=[
            "WorkerScanID",
            "WorkerID",
            "LineID",
            "MachineID",
            "WorkerOperations",
            "CreatedAt",
            "UpdatedAt",
            "HasExpired",
            "EndedAt",
        ],
    )
    worker_scan_table = worker_scan_table.astype(
        {
            "WorkerScanID": "int64",
            "WorkerID": "Int64",
            "LineID": "Int64",
            "MachineID": "Int64",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
            "HasExpired": "Int64",
            "EndedAt": "datetime64[ns]",
        }
    )
    # worker_scan_table["WorkerOperations"] = worker_scan_table["WorkerOperations"].to_json()

    line_table = pd.DataFrame(
        line, columns=["LineID", "LineCode", "LineDescription", "CreatedAt", "UpdatedAt"]
    )
    line_table = line_table.astype(
        {
            "LineID": "Int64",
            "LineCode": "string",
            "LineDescription": "string",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
        }
    )

    worker_table = pd.DataFrame(
        worker,
        columns=[
            "WorkerID",
            "WorkerCode",
            "WorkerDescription",
            "WorkerImageUrl",
            "WorkerThumbnailUrl",
            "AllocatedMachines",
            "CreatedAt",
            "UpdatedAt",
        ],
    )
    worker_table = worker_table.astype(
        {
            "WorkerID": "Int64",
            "WorkerCode": "string",
            "WorkerDescription": "string",
            "WorkerImageUrl": "string",
            "WorkerThumbnailUrl": "string",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
        }
    )
    # worker_table["AllocatedMachines"] = worker_table["AllocatedMachines"].to_json()

    machine_type_table = pd.DataFrame(
        machine_type,
        columns=[
            "MachineTypeID",
            "MachineTypeCode",
            "MachineTypeDescription",
            "Allowance",
            "CreatedAt",
            "UpdatedAt",
        ],
    )
    machine_type_table = machine_type_table.astype(
        {
            "MachineTypeID": "Int64",
            "MachineTypeCode": "string",
            "MachineTypeDescription": "string",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
            "Allowance": "float",
        }
    )

    operation_table = pd.DataFrame(
        operation,
        columns=[
            "OperationID",
            "OperationCode",
            "OperationName",
            "OperationDescription",
            "Department",
            "PieceRate",
            "OperationType",
            "OperationImageUrl",
            "OperationThumbnailUrl",
            "SectionID",
            "CreatedAt",
            "UpdatedAt",
        ],
    )
    operation_table = operation_table.astype(
        {
            "OperationID": "Int64",
            "OperationCode": "string",
            "OperationName": "string",
            "OperationDescription": "string",
            "Department": "string",
            "PieceRate": "Int64",
            "OperationType": "string",
            "OperationImageUrl": "string",
            "OperationThumbnailUrl": "string",
            "SectionID": "Int64",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
        }
    )

    section_table = pd.DataFrame(
        section,
        columns=[
            "SectionID",
            "SectionCode",
            "SectionDescription",
            "CreatedAt",
            "UpdatedAt",
        ],
    )
    section_table = section_table.astype(
        {
            "SectionID": "Int64",
            "SectionCode": "string",
            "SectionDescription": "string",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
        }
    )

    piece_wise_cut_report_table = pd.DataFrame(
        piece_wise_cut_report,
        columns=["PieceID", "BundleID", "PieceNumber", "CreatedAt", "UpdatedAt"],
    )
    piece_wise_cut_report_table = piece_wise_cut_report_table.astype(
        {
            "PieceID": "Int64",
            "BundleID": "Int64",
            "PieceNumber": "Int64",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
        }
    )

    cut_report_table = pd.DataFrame(
        cut_report,
        columns=[
            "BundleID",
            "BundleCode",
            "BundleQuantity",
            "ScannedQuantity",
            "RemainingQuantity",
            "CutJobID",
            "CreatedAt",
            "UpdatedAt",
        ],
    )
    cut_report_table = cut_report_table.astype(
        {
            "BundleID": "Int64",
            "BundleCode": "string",
            "BundleQuantity": "Int64",
            "ScannedQuantity": "Int64",
            "RemainingQuantity": "Int64",
            "CutJobID": "Int64",
            "CreatedAt" : "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]"        
        }
    )

    cut_job_table = pd.DataFrame(
        cut_job,
        columns=[
            "CutJobID",
            "CutNo",
            "ProductionOrderID",
            "CutQuantity",
            "MarkerID",
            "CreatedAt",
            "UpdatedAt",
        ],
    )
    cut_job_table = cut_job_table.astype(
        {
            "CutJobID": "Int64",
            "CutNo": "Int64",
            "ProductionOrderID": "Int64",
            "CutQuantity": "Int64",
            "MarkerID": "Int64",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
        }
    )

    marker_table = pd.DataFrame(
        marker,
        columns=[
            "MarkerID",
            "MarkerCode",
            "ProductionOrderID",
            "MarkerMapping",
            "CreatedAt",
            "UpdatedAt",
        ],
    )
    marker_table = marker_table.astype(
        {
            "MarkerID": "Int64",
            "MarkerCode": "string",
            "ProductionOrderID": "Int64",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
        }
    )
    # marker_table["MarkerMapping"] = marker_table["MarkerMapping"].to_json()

    production_order_table = pd.DataFrame(
        production_order,
        columns=[
            "ProductionOrderID",
            "ProductionOrderCode",
            "SaleOrderID",
            "StyleTemplateID",
            "IsFollowOperationSequence",
            "CreatedAt",
            "UpdatedAt",
        ],
    )
    production_order_table = production_order_table.astype(
        {
            "ProductionOrderID": "Int64",
            "ProductionOrderCode": "string",
            "SaleOrderID": "Int64",
            "StyleTemplateID": "Int64",
            "IsFollowOperationSequence": "bool",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
        }
    )

    sale_order_table = pd.DataFrame(
        sale_order,
        columns=[
            "SaleOrderID",
            "SaleOrderCode",
            "Customer",
            "OrderQuantity",
            "CreatedAt",
            "UpdatedAt",
        ],
    )
    sale_order_table = sale_order_table.astype(
        {
            "SaleOrderID": "Int64",
            "SaleOrderCode": "string",
            "Customer": "string",
            "OrderQuantity": "Int64",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
        }
    )

    style_template_table = pd.DataFrame(
        style_template,
        columns=["StyleTemplateID", "StyleTemplateCode", "CreatedAt", "UpdatedAt"],
    )
    style_template_table = style_template_table.astype(
        {
            "StyleTemplateID": "Int64",
            "StyleTemplateCode": "string",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
        }
    )

    module_table = pd.DataFrame(
        module, columns=["ModuleID", "ModuleCode", "CreatedAt", "UpdatedAt"]
    )
    module_table = module_table.astype(
        {
            "ModuleID": "Int64",
            "ModuleCode": "string",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
        }
    )

    userpermission_table = pd.DataFrame(
        userpermission,
        columns=["UserPermissionID", "UserID", "ModuleID", "CreatedAt", "UpdatedAt"],
    )
    userpermission_table = userpermission_table.astype(
        {
            "UserPermissionID": "Int64",
            "UserID": "Int64",
            "ModuleID": "Int64",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
        }
    )

    style_bulletin_table = pd.DataFrame(
        style_bulletin,
        columns=[
            "StyleBulletinID",
            "StyleTemplateID",
            "OperationID",
            "OperationSequence",
            "ScanType",
            "IsFirst",
            "IsLast",
            "MachineTypeID",
            "CreatedAt",
            "UpdatedAt",
        ],
    )
    style_bulletin_table = style_bulletin_table.astype(
        {
            "StyleBulletinID": "Int64",
            "StyleTemplateID": "Int64",
            "OperationID": "Int64",
            "OperationSequence": "Int64",
            "ScanType": "string",
            "IsFirst": "bool",
            "IsLast": "bool",
            "MachineTypeID": "Int64",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
        }
    )

    user_table = pd.DataFrame(
        user,
        columns=[
            "UserID",
            "UserName",
            "Password",
            "UserType",
            "LineID",
            "SectionID",
            "CreatedAt",
            "UpdatedAt",
        ],
    )
    user_table = user_table.astype(
        {
            "UserID": "Int64",
            "UserName": "string",
            "Password": "string",
            "UserType": "string",
            "LineID": "Int64",
            "SectionID": "Int64",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
        }
    )

    tag_table = pd.DataFrame(tag, columns=["TagID", "BundleID", "CreatedAt", "UpdatedAt","PieceID","GroupID"])
    tag_table = tag_table.astype(
        {
            "TagID": "Int64",
            "BundleID": "Int64",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
            "PieceID":"Int64",
            "GroupID":"Int64",
        }
    )

    #DENORMALIZATION

    machine_table_denorm = machine_table.merge(line_table, how="left", on="LineID").drop(
    ["CreatedAt_y", "UpdatedAt_y"], axis=1
)

    machine_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt"}, axis=1, inplace=True
    )


    machine_table_denorm = machine_table_denorm.merge(
        worker_table, how="left", left_on="ActiveWorkerID", right_on="WorkerID"
    ).drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)

    machine_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt"}, axis=1, inplace=True
    )


    machine_table_denorm = machine_table_denorm.merge(
        machine_type_table, how="left", on="MachineTypeID"
    ).drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)

    machine_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt"}, axis=1, inplace=True
    )

    worker_scan_table_denorm = worker_scan_table.merge(line_table, how="left", on="LineID").drop(
        ["CreatedAt_y", "UpdatedAt_y"], axis=1
    )

    worker_scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt"}, axis=1, inplace=True
    )


    worker_scan_table_denorm = worker_scan_table_denorm.merge(
        worker_table, how="left", on="WorkerID"
    ).drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)

    worker_scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt"}, axis=1, inplace=True
    )


    worker_scan_table_denorm = worker_scan_table_denorm.merge(
        machine_table_denorm, how="left", on="MachineID"
    ).drop(["CreatedAt_y", "UpdatedAt_y",'LineCode_y',
        'LineDescription_y', 'WorkerID_y', 'WorkerCode_y',
        'WorkerDescription_y', 'WorkerImageUrl_y', 'WorkerThumbnailUrl_y',
        'AllocatedMachines_y','LineID_y'], axis=1)

    worker_scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt",'LineCode_x':'LineCode', 'LineDescription_x':'LineDescription', 'WorkerCode_x':'WorkerCode',
        'WorkerDescription_x':'WorkerDescription', 'WorkerImageUrl_x':'WorkerImageUrl', 'WorkerThumbnailUrl_x':'WorkerThumbnailUrl',
        'AllocatedMachines_x':'AllocatedMachines','WorkerID_x':'WorkerID', 'LineID_x':'LineID'}, axis=1, inplace=True
    )
    operation_table_denorm=(
        operation_table.merge(section_table, how="left", on="SectionID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )

    operation_table_denorm.rename({'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    production_order_table_denorm = (
        production_order_table.merge(sale_order_table, how="left", on="SaleOrderID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
        .merge(style_template_table, how="left", on="StyleTemplateID")
        .drop(["CreatedAt", "UpdatedAt"], axis=1)
    )

    production_order_table_denorm.rename({'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)


    marker_table_denorm = (
        marker_table.merge(production_order_table_denorm, how="left", on="ProductionOrderID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )

    marker_table_denorm.rename({'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)


    cut_job_table_denorm = (
        cut_job_table.merge(production_order_table_denorm, how="left", on="ProductionOrderID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )
    cut_job_table_denorm.rename({'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    cut_job_table_denorm= cut_job_table_denorm.merge(marker_table_denorm, how="left", on="MarkerID")
    cut_job_table_denorm.drop(["CreatedAt_y", "UpdatedAt_y",'CreatedAt_y', 'UpdatedAt_y',
        'ProductionOrderCode_y', 'SaleOrderID_y', 'StyleTemplateID_y',
        'IsFollowOperationSequence_y', 'SaleOrderCode_y', 'Customer_y',
        'OrderQuantity_y', 'StyleTemplateCode_y','ProductionOrderID_y'], axis=1, inplace=True)


    cut_job_table_denorm.rename({'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt','ProductionOrderCode_x':'ProductionOrderCode', 'SaleOrderID_x':'SaleOrderID',
        'StyleTemplateID_x':'StyleTemplateID', 'IsFollowOperationSequence_x':'IsFollowOperationSequence', 'SaleOrderCode_x':'SaleOrderCode',
        'Customer_x':'Customer', 'OrderQuantity_x':'OrderQuantity', 'StyleTemplateCode_x':'StyleTemplateCode','ProductionOrderID_x':'ProductionOrderID'}, axis=1, inplace=True)

    cut_report_table_denorm=(
        cut_report_table.merge(cut_job_table_denorm, how="left", on="CutJobID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )

    cut_report_table_denorm.rename({'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    piece_wise_cut_report_table_denorm=(
        piece_wise_cut_report_table.merge(cut_report_table_denorm, how="left", on="BundleID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )

    piece_wise_cut_report_table_denorm.rename({'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    scan_table_denorm = scan_table.merge(line_table, how="left", on="LineID").drop(
        ["CreatedAt_y", "UpdatedAt_y"], axis=1
    )

    scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt"}, axis=1, inplace=True
    )


    scan_table_denorm = scan_table_denorm.merge(
        worker_table, how="left", on="WorkerID"
    ).drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)

    scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt"}, axis=1, inplace=True
    )


    scan_table_denorm = scan_table_denorm.merge(
        cut_report_table_denorm, how="left", on="BundleID"
    ).drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)

    scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt"}, axis=1, inplace=True
    )


    scan_table_denorm = scan_table_denorm.merge(
        machine_table_denorm, how="left", on="MachineID"
    ).drop(["CreatedAt_y", "UpdatedAt_y",'LineCode_y', 'LineDescription_y', 'WorkerID_y', 'WorkerCode_y',
        'WorkerDescription_y', 'WorkerImageUrl_y', 'WorkerThumbnailUrl_y',
        'AllocatedMachines_y','LineID_y'], axis=1)
    scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt",'LineID_x':'LineID',
        'LineCode_x':'LineCode', 'LineDescription_x':'LineDescription', 'WorkerID_x':'WorkerID', 'WorkerCode_x':'WorkerCode',
        'WorkerDescription_x':'WorkerDescription', 'WorkerImageUrl_x':'WorkerImageUrl', 'WorkerThumbnailUrl_x':'WorkerThumbnailUrl',
        'AllocatedMachines_x':'AllocatedMachines'}, axis=1, inplace=True
    )

    scan_table_denorm = scan_table_denorm.merge(
        operation_table_denorm, how="left", on="OperationID"
    ).drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt"}, axis=1, inplace=True
    )

    scan_table_denorm = scan_table_denorm.merge(
        piece_wise_cut_report_table_denorm, how="left", on="PieceID"
    ).drop(["CreatedAt_y", "UpdatedAt_y",'BundleCode_y', 'BundleQuantity_y',
        'ScannedQuantity_y', 'RemainingQuantity_y', 'CutJobID_y', 'CutNo_y',
        'ProductionOrderID_y', 'CutQuantity_y', 'MarkerID_y',
        'ProductionOrderCode_y', 'SaleOrderID_y', 'StyleTemplateID_y',
        'IsFollowOperationSequence_y', 'SaleOrderCode_y', 'Customer_y',
        'OrderQuantity_y', 'StyleTemplateCode_y', 'MarkerCode_y',
        'MarkerMapping_y','BundleID_y'], axis=1)
    scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt", 'BundleID_x':'BundleID', 'BundleCode_x':'BundleCode',
        'BundleQuantity_x':'BundleQuantity', 'ScannedQuantity_x':'ScannedQuantity', 'RemainingQuantity_x':'RemainingQuantity',
        'CutJobID_x':'CutJobID', 'CutNo_x':'CutNo', 'ProductionOrderID_x':'ProductionOrderID', 'CutQuantity_x':'CutQuantity',
        'MarkerID_x':'MarkerID', 'ProductionOrderCode_x':'ProductionOrderCode', 'SaleOrderID_x':'SaleOrderID',
        'StyleTemplateID_x':'StyleTemplateID', 'IsFollowOperationSequence_x':'IsFollowOperationSequence', 'SaleOrderCode_x':'SaleOrderCode',
        'Customer_x':'Customer', 'OrderQuantity_x':'OrderQuantity', 'StyleTemplateCode_x':'StyleTemplateCode', 'MarkerCode_x':'MarkerCode',
        'MarkerMapping_x':'MarkerMapping'}, axis=1, inplace=True
    )


    scan_table_denorm = scan_table_denorm.merge(
        worker_scan_table_denorm, how="left", on="WorkerScanID"
    ).drop(["CreatedAt_y", "UpdatedAt_y",
        'WorkerID_y', 'LineID_y', 'MachineID_y','LineCode_y', 'LineDescription_y',
        'WorkerCode_y', 'WorkerDescription_y', 'WorkerImageUrl_y',
        'WorkerThumbnailUrl_y', 'AllocatedMachines_y', 'MachineCode_y',
        'MachineDescription_y', 'MachineImageUrl_y', 'MachineThumbnailUrl_y',
        'MachineTypeID_y', 'ActiveWorkerID_y', 'Operations_y', 'BoxID_y',
        'MachineTypeCode_y', 'MachineTypeDescription_y', 'Allowance_y'], axis=1)
    scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt",'MachineID_x':'MachineID', 'MachineCode_x':'MachineCode', 'MachineDescription_x':'MachineDescription',
        'MachineImageUrl_x':'MachineImageUrl', 'MachineThumbnailUrl_x':'MachineThumbnailUrl', 'MachineTypeID_x':'MachineTypeID',
        'ActiveWorkerID_x':'ActiveWorkerID', 'Operations_x':'Operations', 'BoxID_x':'BoxID', 'MachineTypeCode_x':'MachineTypeCode',
        'MachineTypeDescription_x':'MachineTypeDescription', 'Allowance_x':'Allowance','LineID_x':'LineID', 'LineCode_x':'LineCode', 'LineDescription_x':'LineDescription',
        'WorkerID_x':'WorkerID', 'WorkerCode_x':'WorkerCode', 'WorkerDescription_x':'WorkerDescription', 'WorkerImageUrl_x':'WorkerImageUrl',
        'WorkerThumbnailUrl_x':'WorkerThumbnailUrl', 'AllocatedMachines_x':'AllocatedMachines'}, axis=1, inplace=True
    )

    piece_wise_scan_table_denorm = piece_wise_scan_table.merge(
        piece_wise_cut_report_table_denorm, how="left", on="PieceID"
    ).drop(["CreatedAt_y", "UpdatedAt_y",'BundleID_y'], axis=1)

    piece_wise_scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt",'BundleID_x':'BundleID'}, axis=1, inplace=True
    )

    piece_wise_scan_table_denorm = piece_wise_scan_table_denorm.merge(
        operation_table_denorm, how="left", on="OperationID"
    ).drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)

    piece_wise_scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt"}, axis=1, inplace=True
    )

    piece_wise_scan_table_denorm = piece_wise_scan_table_denorm.merge(
        scan_table_denorm, how="left", on="ScanID"
    ).drop(["CreatedAt_y", "UpdatedAt_y",'OperationCode_y',
        'OperationName_y', 'OperationDescription_y', 'Department_y',
        'PieceRate_y', 'OperationType_y', 'OperationImageUrl_y',
        'OperationThumbnailUrl_y', 'SectionID_y', 'SectionCode_y',
        'SectionDescription_y', 'PieceNumber_y', 'BundleCode_y',
        'BundleQuantity_y', 'ScannedQuantity_y', 'RemainingQuantity_y',
        'CutJobID_y', 'CutNo_y', 'ProductionOrderID_y', 'CutQuantity_y',
        'MarkerID_y', 'ProductionOrderCode_y', 'SaleOrderID_y',
        'StyleTemplateID_y', 'IsFollowOperationSequence_y', 'SaleOrderCode_y',
        'Customer_y', 'OrderQuantity_y', 'StyleTemplateCode_y', 'MarkerCode_y',
        'MarkerMapping_y','OperationID_y', 'PieceID_y','BundleID_y', 'MachineID_y', 'LineID_y', 'WorkerID_y'], axis=1)
    piece_wise_scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt",'OperationCode_x':'OperationCode',
        'OperationName_x':'OperationName', 'OperationDescription_x':'OperationDescription', 'Department_x':'Department',
        'PieceRate_x':'PieceRate', 'OperationType_x':'OperationType', 'OperationImageUrl_x':'OperationImageUrl',
        'OperationThumbnailUrl_x':'OperationThumbnailUrl', 'SectionID_x':'SectionID', 'SectionCode_x':'SectionCode',
        'SectionDescription_x':'SectionDescription', 'PieceNumber_x':'PieceNumber', 'BundleCode_x':'BundleCode',
        'BundleQuantity_x':'BundleQuantity', 'ScannedQuantity_x':'ScannedQuantity', 'RemainingQuantity_x':'RemainingQuantity',
        'CutJobID_x':'CutJobID', 'CutNo_x':'CutNo', 'ProductionOrderID_x':'ProductionOrderID', 'CutQuantity_x':'CutQuantity',
        'MarkerID_x':'MarkerID', 'ProductionOrderCode_x':'ProductionOrderCode', 'SaleOrderID_x':'SaleOrderID',
        'StyleTemplateID_x':'StyleTemplateID', 'IsFollowOperationSequence_x':'IsFollowOperationSequence', 'SaleOrderCode_x':'SaleOrderCode',
        'Customer_x':'Customer', 'OrderQuantity_x':'OrderQuantity', 'StyleTemplateCode_x':'StyleTemplateCode', 'MarkerCode_x':'MarkerCode',
        'MarkerMapping_x':'MarkerMapping','OperationID_x':'OperationID', 'PieceID_x':'PieceID','BundleID_x':'BundleID', 'MachineID_x':'MachineID', 'LineID_x':'LineID','WorkerID_x':'WorkerID'}, axis=1, inplace=True
    )

    piece_wise_scan_table_denorm = piece_wise_scan_table_denorm.merge(
        cut_report_table_denorm, how="left", on="BundleID"
    ).drop(["CreatedAt_y", "UpdatedAt_y",
    'BundleCode_y',
        'BundleQuantity_y', 'ScannedQuantity_y', 'RemainingQuantity_y',
        'CutJobID_y', 'CutNo_y', 'ProductionOrderID_y', 'CutQuantity_y',
        'MarkerID_y', 'ProductionOrderCode_y', 'SaleOrderID_y',
        'StyleTemplateID_y', 'IsFollowOperationSequence_y', 'SaleOrderCode_y',
        'Customer_y', 'OrderQuantity_y', 'StyleTemplateCode_y', 'MarkerCode_y',
        'MarkerMapping_y'], axis=1)

    piece_wise_scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt",'BundleCode_x':'BundleCode',
        'BundleQuantity_x':'BundleQuantity', 'ScannedQuantity_x':'ScannedQuantity', 'RemainingQuantity_x':'RemainingQuantity',
        'CutJobID_x':'CutJobID', 'CutNo_x':'CutNo', 'ProductionOrderID_x':'ProductionOrderID', 'CutQuantity_x':'CutQuantity',
        'MarkerID_x':'MarkerID', 'ProductionOrderCode_x':'ProductionOrderCode', 'SaleOrderID_x':'SaleOrderID',
        'StyleTemplateID_x':'StyleTemplateID', 'IsFollowOperationSequence_x':'IsFollowOperationSequence', 'SaleOrderCode_x':'SaleOrderCode',
        'Customer_x':'Customer', 'OrderQuantity_x':'OrderQuantity', 'StyleTemplateCode_x':'StyleTemplateCode', 'MarkerCode_x':'MarkerCode',
        'MarkerMapping_x':'MarkerMapping'}, axis=1, inplace=True
    )

    style_bulletin_table_denorm = style_bulletin_table.merge(
        style_template_table, how="left", on="StyleTemplateID"
    ).drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)

    style_bulletin_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt"}, axis=1, inplace=True
    )

    style_bulletin_table_denorm = style_bulletin_table_denorm.merge(
        operation_table_denorm, how="left", on="OperationID"
    ).drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)

    style_bulletin_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt"}, axis=1, inplace=True
    )


    style_bulletin_table_denorm = style_bulletin_table_denorm.merge(
        machine_type_table, how="left", on="MachineTypeID"
    ).drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)

    style_bulletin_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt"}, axis=1, inplace=True
    )

    operation_table_denorm=(
        operation_table.merge(section_table, how="left", on="SectionID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )

    operation_table_denorm.rename({'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    tag_table_denorm=(
        tag_table.merge(cut_report_table_denorm, how="left", on="BundleID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )

    tag_table_denorm.rename({'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)


    user_table_denorm = (
        user_table.merge(line_table, how="left", on="LineID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )
    user_table_denorm.rename({'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)



    user_table_denorm = (
        user_table_denorm.merge(section_table, how="left", on="SectionID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )
    user_table_denorm.rename({'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)


    userpermission_table_denorm = (
        userpermission_table.merge(module_table, how="left", on="ModuleID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )
    userpermission_table_denorm.rename({'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)


    userpermission_table_denorm = (
        userpermission_table_denorm.merge(user_table_denorm, how="left", on="UserID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )
    userpermission_table_denorm.rename({'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    #UPDATE
    
    myupdate("line",line_table,"LineID")

    myupdate('module',module_table,"ModuleID")
    myupdate('userpermission',userpermission_table_denorm,"UserPermissionID")
    
    myupdate('worker',worker_table,"WorkerID")
    myupdate('machine_type',machine_type_table,"MachineTypeID")
    myupdate('machine',machine_table_denorm,"MachineID")
    myupdate('sale_order',sale_order_table,"SaleOrderID")

    myupdate('section',section_table,"SectionID")
    myupdate('user',user_table_denorm,"UserID")
    myupdate('operation',operation_table_denorm,"OperationID")

    myupdate('worker_scan',worker_scan_table_denorm,"WorkerScanID")
    myupdate('style_template',style_template_table,"StyleTemplateID")

    myupdate('style_bulletin',style_bulletin_table_denorm,"StyleBulletinID")
    myupdate('production_order',production_order_table_denorm,"ProductionOrderID")
    myupdate('marker',marker_table_denorm,"MarkerID")

    myupdate('cut_job',cut_job_table_denorm,"CutJobID")
    myupdate('cut_report',cut_report_table_denorm,"BundleID")
    myupdate('tag',tag_table_denorm,"TagID")

    myupdate('scan',scan_table_denorm,"ScanID")
    myupdate('piece_wise_scan',piece_wise_scan_table_denorm,"PieceWiseScanningID")
    myupdate('piece_wise_cut_report',piece_wise_cut_report_table_denorm,"PieceID")

    return {"status":"all data updated"}





