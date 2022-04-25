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
from sqlalchemy.types import Integer, Float, String, JSON, DateTime, BINARY, LargeBinary, Boolean
from sqlalchemy.orm import relationship
import os
import psycopg2
import numpy as np
import psycopg2.extras as extras
from io import StringIO
import sys
from tests import mysqlRowcount, postgresRowcount
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


def create_logic():
    return {'Status': 'created'}


# ------------------------------------------------------------
# INSERTION LOGIC
connection = engine_postgres.raw_connection()
conn = connection
tmp_df = "./tmp_dataframe.tsv"


def myinsert(table, df, batch_size=50000, data_threshold=100000):
    '''
    arguments:
    table:str of table name.
    df:table name.
    data_threshold:integer from which to start inserting in batches.
    batch_size: integer to set the batch size for inserting.

    e.g:
    table='line'
    df=line_table
    data_threshold=100
    batch_size=10
    '''

    df = df.set_index(df.columns[0], inplace=False, drop=True)
    count = 0
    for i in range(len(df)):
        # check if the postgres database is empty.
        if [] == session_postgres.execute(f'select "CreatedAt" from public.{table} order by "CreatedAt" desc limit 1').all():
            df.to_csv(tmp_df, sep='\t', na_rep='NULL', index_label="id",
                      header=False, quoting=csv.QUOTE_NONE, quotechar="", escapechar="\\")
            f = open(tmp_df, "r")
            cursor = conn.cursor()
            try:
                cursor.copy_from(f, table, sep="\t", null='NULL')
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s" % error)
                conn.rollback()
                cursor.close()
            f.close()
            os.remove(tmp_df)
            print(i + 1, f"{table} First Bulk Insert! database was empty")
            break

        # Batch_insert for new data
        elif session_postgres.execute(f'select "CreatedAt" from public.{table} order by "CreatedAt" desc limit 1').all()[0][0] < df.iloc[i, df.columns.get_loc("CreatedAt")].to_pydatetime() and count < 1:
            print("Database has already some data", i)
            count += 1

            # set the minimum lenght of dataframe
            # data_threshold=100

            # if new dataframe lenght is less than data_threshold then dump all data
            if len(df.iloc[i:, :]) < data_threshold:
                df.iloc[i:, :].to_csv(tmp_df, sep='\t', index_label="id", header=False,
                                      na_rep='NULL', quoting=csv.QUOTE_NONE, quotechar="", escapechar="\\")
                f = open(tmp_df, "r")
                cursor = conn.cursor()
                try:
                    cursor.copy_from(f, table, sep="\t", null='NULL')
                    conn.commit()
                except (Exception, psycopg2.DatabaseError) as error:
                    print("Error: %s" % error)
                    conn.rollback()
                    cursor.close()
                f.close()
                os.remove(tmp_df)
                print(
                    i + 1, f"{table} database has already some data less than data_threshold {data_threshold}")
                break

            # if new dataframe lenght is greater than data_threshold then dump data in batches
            else:
                # batch_size=100
                for j in range(batch_size, len(df.iloc[i:, :]), batch_size):
                    df.iloc[i:i+batch_size, :].to_csv(tmp_df, sep='\t', index_label="id", header=False,
                                                      na_rep='NULL', quoting=csv.QUOTE_NONE, quotechar="", escapechar="\\")
                    f = open(tmp_df, "r")
                    cursor = conn.cursor()
                    try:
                        cursor.copy_from(f, table, sep="\t", null='NULL')
                        conn.commit()
                        i = i+batch_size
                        print(
                            f"========Data inserted from index{i}to{i+batch_size}")
                    except (Exception, psycopg2.DatabaseError) as error:
                        print("Error: %s" % error)
                        conn.rollback()
                        cursor.close()
                    f.close()
                    os.remove(tmp_df)
                    print(
                        i + 1, f"Inserted data greater than {data_threshold}")

        else:
            print(i + 1, f"{table} upto-date")

    return f"Successfully performed myinsert() on {table}"
# ------------------------------------------------------------
# INSERTION


def insert_logic():

    piece_wise_scan = session_mysql.execute(
        "select * from piece_wise_scan").all()
    piece_wise_cut_report = session_mysql.execute(
        "select * from piece_wise_cut_report"
    ).all()
    cut_report = session_mysql.execute("select * from cut_report").all()
    cut_job = session_mysql.execute("select * from cut_job").all()
    production_order = session_mysql.execute(
        "select * from production_order").all()
    sale_order = session_mysql.execute("select * from sale_order").all()
    style_template = session_mysql.execute(
        "select * from style_template").all()
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
    userpermission = session_mysql.execute(
        "select * from userpermission").all()

    style_bulletin = session_mysql.execute("select * from style_bulletin")
    tag = session_mysql.execute("select * from tag")
    user = session_mysql.execute("select * from user")

    box = session_mysql.execute("select * from box")
    machine_down_time = session_mysql.execute(
        "select * from machine_down_time")
    line_layout = session_mysql.execute("select * from line_layout")
    scan_group = session_mysql.execute("select * from scan_group")
    piece_wise_group = session_mysql.execute("select * from piece_wise_group")

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
            "IsMachineDown": "bool"
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
            "GroupID"
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
            "GroupID":"int64",
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
        line, columns=["LineID", "LineCode",
                       "LineDescription", "CreatedAt", "UpdatedAt"]
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
        columns=["PieceID", "BundleID",
                 "PieceNumber", "CreatedAt", "UpdatedAt"],
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
            "CreatedAt": "datetime64[ns]",
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
        columns=["StyleTemplateID", "StyleTemplateCode",
                 "CreatedAt", "UpdatedAt"],
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
        columns=["UserPermissionID", "UserID",
                 "ModuleID", "CreatedAt", "UpdatedAt"],
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

    tag_table = pd.DataFrame(tag, columns=["TagID", "BundleID", "CreatedAt", "UpdatedAt", "PieceID",
                                           "GroupID"])
    tag_table = tag_table.astype(
        {
            "TagID": "Int64",
            "BundleID": "Int64",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
            "PieceID": "Int64",
            "GroupID": "Int64"
        }
    )

    box_table = pd.DataFrame(
        box,
        columns=[
            "BoxID",
            "BoxCode",
            "IssueDate",
            "CreatedAt",
            "UpdatedAt",

        ],
    )
    box_table = box_table.astype(
        {
            "BoxID": "Int64",
            "BoxCode": "string",
            "IssueDate": "datetime64[ns]",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]"

        }
    )

    piece_wise_group_table = pd.DataFrame(
        piece_wise_group,
        columns=[
            "PieceWiseGroupID",
            "GroupID",
            "BundleID",
            "PieceID",
            "CreatedAt",
            "UpdatedAt",
            "GroupName",

        ],
    )
    piece_wise_group_table = piece_wise_group_table.astype(
        {
            "PieceWiseGroupID": "Int64",
            "GroupID": "Int64",
            "BundleID": "Int64",
            "PieceID": "Int64",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",
            "GroupName": "string",

        }
    )

    scan_group_table = pd.DataFrame(
        scan_group,
        columns=[

            "GroupID",
            "CreatedAt",
            "UpdatedAt",

        ],
    )
    scan_group_table = scan_group_table.astype(
        {
            "GroupID": "Int64",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",

        }
    )

    line_layout_table = pd.DataFrame(
        line_layout,
        columns=[

            "LineLayoutID",
            "RevisionNo",
            "LineID",
            "ProductionOrderID",
            "LineLayoutDate",
            "LineLayoutStatus",
            "LineLayoutOperationMachines",
            "IsAnyMachines",
            "ParentLineLayoutID",
            "CreatedAt",
            "UpdatedAt",

        ],
    )
    line_layout_table = line_layout_table.astype(
        {
            "LineLayoutID": "Int64",
            "RevisionNo": "Int64",
            "LineID": "Int64",
            "ProductionOrderID": "Int64",
            "LineLayoutDate": "datetime64[ns]",
            "LineLayoutStatus": "string",
            "IsAnyMachines": "bool",
            "ParentLineLayoutID": "Int64",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",

        }
    )

    machine_down_time_table = pd.DataFrame(
        machine_down_time,
        columns=[

            "MachineDownTimeID",
            "MachineID",
            "DownReason",
            "StartTime",
            "EndTime",
            "CreatedAt",
            "UpdatedAt",

        ],
    )
    machine_down_time_table = machine_down_time_table.astype(
        {
            "MachineID": "Int64",
            "DownReason": "string",
            "StartTime": "datetime64[ns]",
            "EndTime": "datetime64[ns]",
            "CreatedAt": "datetime64[ns]",
            "UpdatedAt": "datetime64[ns]",

        }
    )
    # DENORMALIZATION

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
    ).drop(["CreatedAt_y", "UpdatedAt_y", 'LineCode_y',
            'LineDescription_y', 'WorkerID_y', 'WorkerCode_y',
            'WorkerDescription_y', 'WorkerImageUrl_y', 'WorkerThumbnailUrl_y',
            'AllocatedMachines_y', 'LineID_y'], axis=1)

    worker_scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt", 'LineCode_x': 'LineCode', 'LineDescription_x': 'LineDescription', 'WorkerCode_x': 'WorkerCode',
         'WorkerDescription_x': 'WorkerDescription', 'WorkerImageUrl_x': 'WorkerImageUrl', 'WorkerThumbnailUrl_x': 'WorkerThumbnailUrl',
         'AllocatedMachines_x': 'AllocatedMachines', 'WorkerID_x': 'WorkerID', 'LineID_x': 'LineID'}, axis=1, inplace=True
    )
    operation_table_denorm = (
        operation_table.merge(section_table, how="left", on="SectionID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )

    operation_table_denorm.rename(
        {'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    production_order_table_denorm = (
        production_order_table.merge(
            sale_order_table, how="left", on="SaleOrderID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
        .merge(style_template_table, how="left", on="StyleTemplateID")
        .drop(["CreatedAt", "UpdatedAt"], axis=1)
    )

    production_order_table_denorm.rename(
        {'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    marker_table_denorm = (
        marker_table.merge(production_order_table_denorm,
                           how="left", on="ProductionOrderID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )

    marker_table_denorm.rename(
        {'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    cut_job_table_denorm = (
        cut_job_table.merge(production_order_table_denorm,
                            how="left", on="ProductionOrderID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )
    cut_job_table_denorm.rename(
        {'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    cut_job_table_denorm = cut_job_table_denorm.merge(
        marker_table_denorm, how="left", on="MarkerID")
    cut_job_table_denorm.drop(["CreatedAt_y", "UpdatedAt_y", 'CreatedAt_y', 'UpdatedAt_y',
                               'ProductionOrderCode_y', 'SaleOrderID_y', 'StyleTemplateID_y',
                               'IsFollowOperationSequence_y', 'SaleOrderCode_y', 'Customer_y',
                               'OrderQuantity_y', 'StyleTemplateCode_y', 'ProductionOrderID_y'], axis=1, inplace=True)

    cut_job_table_denorm.rename({'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt', 'ProductionOrderCode_x': 'ProductionOrderCode', 'SaleOrderID_x': 'SaleOrderID',
                                 'StyleTemplateID_x': 'StyleTemplateID', 'IsFollowOperationSequence_x': 'IsFollowOperationSequence', 'SaleOrderCode_x': 'SaleOrderCode',
                                 'Customer_x': 'Customer', 'OrderQuantity_x': 'OrderQuantity', 'StyleTemplateCode_x': 'StyleTemplateCode', 'ProductionOrderID_x': 'ProductionOrderID'}, axis=1, inplace=True)

    cut_report_table_denorm = (
        cut_report_table.merge(cut_job_table_denorm, how="left", on="CutJobID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )

    cut_report_table_denorm.rename(
        {'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    piece_wise_cut_report_table_denorm = (
        piece_wise_cut_report_table.merge(
            cut_report_table_denorm, how="left", on="BundleID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )

    piece_wise_cut_report_table_denorm.rename(
        {'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

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
    ).drop(["CreatedAt_y", "UpdatedAt_y", 'LineCode_y', 'LineDescription_y', 'WorkerID_y', 'WorkerCode_y',
            'WorkerDescription_y', 'WorkerImageUrl_y', 'WorkerThumbnailUrl_y',
            'AllocatedMachines_y', 'LineID_y'], axis=1)
    scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt", 'LineID_x': 'LineID',
         'LineCode_x': 'LineCode', 'LineDescription_x': 'LineDescription', 'WorkerID_x': 'WorkerID', 'WorkerCode_x': 'WorkerCode',
         'WorkerDescription_x': 'WorkerDescription', 'WorkerImageUrl_x': 'WorkerImageUrl', 'WorkerThumbnailUrl_x': 'WorkerThumbnailUrl',
         'AllocatedMachines_x': 'AllocatedMachines'}, axis=1, inplace=True
    )

    scan_table_denorm = scan_table_denorm.merge(
        operation_table_denorm, how="left", on="OperationID"
    ).drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt"}, axis=1, inplace=True
    )

    scan_table_denorm = scan_table_denorm.merge(
        piece_wise_cut_report_table_denorm, how="left", on="PieceID"
    ).drop(["CreatedAt_y", "UpdatedAt_y", 'BundleCode_y', 'BundleQuantity_y',
            'ScannedQuantity_y', 'RemainingQuantity_y', 'CutJobID_y', 'CutNo_y',
            'ProductionOrderID_y', 'CutQuantity_y', 'MarkerID_y',
            'ProductionOrderCode_y', 'SaleOrderID_y', 'StyleTemplateID_y',
            'IsFollowOperationSequence_y', 'SaleOrderCode_y', 'Customer_y',
            'OrderQuantity_y', 'StyleTemplateCode_y', 'MarkerCode_y',
            'MarkerMapping_y', 'BundleID_y'], axis=1)
    scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt", 'BundleID_x': 'BundleID', 'BundleCode_x': 'BundleCode',
         'BundleQuantity_x': 'BundleQuantity', 'ScannedQuantity_x': 'ScannedQuantity', 'RemainingQuantity_x': 'RemainingQuantity',
         'CutJobID_x': 'CutJobID', 'CutNo_x': 'CutNo', 'ProductionOrderID_x': 'ProductionOrderID', 'CutQuantity_x': 'CutQuantity',
         'MarkerID_x': 'MarkerID', 'ProductionOrderCode_x': 'ProductionOrderCode', 'SaleOrderID_x': 'SaleOrderID',
         'StyleTemplateID_x': 'StyleTemplateID', 'IsFollowOperationSequence_x': 'IsFollowOperationSequence', 'SaleOrderCode_x': 'SaleOrderCode',
         'Customer_x': 'Customer', 'OrderQuantity_x': 'OrderQuantity', 'StyleTemplateCode_x': 'StyleTemplateCode', 'MarkerCode_x': 'MarkerCode',
         'MarkerMapping_x': 'MarkerMapping'}, axis=1, inplace=True
    )

    scan_table_denorm = scan_table_denorm.merge(
        worker_scan_table_denorm, how="left", on="WorkerScanID"
    ).drop(["CreatedAt_y", "UpdatedAt_y",
            'WorkerID_y', 'LineID_y', 'MachineID_y', 'LineCode_y', 'LineDescription_y',
            'WorkerCode_y', 'WorkerDescription_y', 'WorkerImageUrl_y',
            'WorkerThumbnailUrl_y', 'AllocatedMachines_y', 'MachineCode_y',
            'MachineDescription_y', 'MachineImageUrl_y', 'MachineThumbnailUrl_y',
            'MachineTypeID_y', 'ActiveWorkerID_y', 'Operations_y', 'BoxID_y',
            'MachineTypeCode_y', 'MachineTypeDescription_y', 'Allowance_y'], axis=1)
    scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt", 'MachineID_x': 'MachineID', 'MachineCode_x': 'MachineCode', 'MachineDescription_x': 'MachineDescription',
         'MachineImageUrl_x': 'MachineImageUrl', 'MachineThumbnailUrl_x': 'MachineThumbnailUrl', 'MachineTypeID_x': 'MachineTypeID',
         'ActiveWorkerID_x': 'ActiveWorkerID', 'Operations_x': 'Operations', 'BoxID_x': 'BoxID', 'MachineTypeCode_x': 'MachineTypeCode',
         'MachineTypeDescription_x': 'MachineTypeDescription', 'Allowance_x': 'Allowance', 'LineID_x': 'LineID', 'LineCode_x': 'LineCode', 'LineDescription_x': 'LineDescription',
         'WorkerID_x': 'WorkerID', 'WorkerCode_x': 'WorkerCode', 'WorkerDescription_x': 'WorkerDescription', 'WorkerImageUrl_x': 'WorkerImageUrl',
         'WorkerThumbnailUrl_x': 'WorkerThumbnailUrl', 'AllocatedMachines_x': 'AllocatedMachines'}, axis=1, inplace=True
    )

    piece_wise_group_table_denorm = (
        piece_wise_group_table.merge(
            scan_group_table, how="left", on="GroupID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )

    piece_wise_group_table_denorm.rename(
        {'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    piece_wise_group_table_denorm = (
        piece_wise_group_table_denorm.merge(
            piece_wise_cut_report_table_denorm, how="left", on="PieceID")
        .drop(["CreatedAt_y", "UpdatedAt_y", 'BundleID_y'], axis=1)
    )

    piece_wise_group_table_denorm.rename(
        {'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt', 'BundleID_x': 'BundleID'}, axis=1, inplace=True)

    piece_wise_scan_table_denorm = piece_wise_scan_table.merge(
        piece_wise_cut_report_table_denorm, how="left", on="PieceID"
    ).drop(["CreatedAt_y", "UpdatedAt_y", 'BundleID_y'], axis=1)

    piece_wise_scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt", 'BundleID_x': 'BundleID'}, axis=1, inplace=True
    )

    piece_wise_scan_table_denorm = piece_wise_scan_table_denorm.merge(
        operation_table_denorm, how="left", on="OperationID"
    ).drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)

    piece_wise_scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt"}, axis=1, inplace=True
    )

    piece_wise_scan_table_denorm = piece_wise_scan_table_denorm.merge(
        scan_table_denorm, how="left", on="ScanID"
    ).drop(["CreatedAt_y", "UpdatedAt_y", 'OperationCode_y',
            'OperationName_y', 'OperationDescription_y', 'Department_y',
            'PieceRate_y', 'OperationType_y', 'OperationImageUrl_y',
            'OperationThumbnailUrl_y', 'SectionID_y', 'SectionCode_y',
            'SectionDescription_y', 'PieceNumber_y', 'BundleCode_y',
            'BundleQuantity_y', 'ScannedQuantity_y', 'RemainingQuantity_y',
            'CutJobID_y', 'CutNo_y', 'ProductionOrderID_y', 'CutQuantity_y',
            'MarkerID_y', 'ProductionOrderCode_y', 'SaleOrderID_y',
            'StyleTemplateID_y', 'IsFollowOperationSequence_y', 'SaleOrderCode_y',
            'Customer_y', 'OrderQuantity_y', 'StyleTemplateCode_y', 'MarkerCode_y',
            'MarkerMapping_y', 'OperationID_y', 'PieceID_y', 'BundleID_y', 'MachineID_y', 'LineID_y', 'WorkerID_y'], axis=1)
    piece_wise_scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt", 'OperationCode_x': 'OperationCode',
         'OperationName_x': 'OperationName', 'OperationDescription_x': 'OperationDescription', 'Department_x': 'Department',
         'PieceRate_x': 'PieceRate', 'OperationType_x': 'OperationType', 'OperationImageUrl_x': 'OperationImageUrl',
         'OperationThumbnailUrl_x': 'OperationThumbnailUrl', 'SectionID_x': 'SectionID', 'SectionCode_x': 'SectionCode',
         'SectionDescription_x': 'SectionDescription', 'PieceNumber_x': 'PieceNumber', 'BundleCode_x': 'BundleCode',
         'BundleQuantity_x': 'BundleQuantity', 'ScannedQuantity_x': 'ScannedQuantity', 'RemainingQuantity_x': 'RemainingQuantity',
         'CutJobID_x': 'CutJobID', 'CutNo_x': 'CutNo', 'ProductionOrderID_x': 'ProductionOrderID', 'CutQuantity_x': 'CutQuantity',
         'MarkerID_x': 'MarkerID', 'ProductionOrderCode_x': 'ProductionOrderCode', 'SaleOrderID_x': 'SaleOrderID',
         'StyleTemplateID_x': 'StyleTemplateID', 'IsFollowOperationSequence_x': 'IsFollowOperationSequence', 'SaleOrderCode_x': 'SaleOrderCode',
         'Customer_x': 'Customer', 'OrderQuantity_x': 'OrderQuantity', 'StyleTemplateCode_x': 'StyleTemplateCode', 'MarkerCode_x': 'MarkerCode',
         'MarkerMapping_x': 'MarkerMapping', 'OperationID_x': 'OperationID', 'PieceID_x': 'PieceID', 'BundleID_x': 'BundleID', 'MachineID_x': 'MachineID', 'LineID_x': 'LineID', 'WorkerID_x': 'WorkerID'}, axis=1, inplace=True
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
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt", 'BundleCode_x': 'BundleCode',
         'BundleQuantity_x': 'BundleQuantity', 'ScannedQuantity_x': 'ScannedQuantity', 'RemainingQuantity_x': 'RemainingQuantity',
         'CutJobID_x': 'CutJobID', 'CutNo_x': 'CutNo', 'ProductionOrderID_x': 'ProductionOrderID', 'CutQuantity_x': 'CutQuantity',
         'MarkerID_x': 'MarkerID', 'ProductionOrderCode_x': 'ProductionOrderCode', 'SaleOrderID_x': 'SaleOrderID',
         'StyleTemplateID_x': 'StyleTemplateID', 'IsFollowOperationSequence_x': 'IsFollowOperationSequence', 'SaleOrderCode_x': 'SaleOrderCode',
         'Customer_x': 'Customer', 'OrderQuantity_x': 'OrderQuantity', 'StyleTemplateCode_x': 'StyleTemplateCode', 'MarkerCode_x': 'MarkerCode',
         'MarkerMapping_x': 'MarkerMapping'}, axis=1, inplace=True
    )
    piece_wise_scan_table_denorm = piece_wise_scan_table_denorm.merge(
        piece_wise_group_table_denorm, how="left", on="GroupID"
    ).drop(["CreatedAt_y", "UpdatedAt_y", 'PieceID_y', 'BundleID_y',
            'IsMachineDown_y', 'PieceNumber_y', 'BundleCode_y',
            'BundleQuantity_y', 'ScannedQuantity_y', 'RemainingQuantity_y',
            'CutJobID_y', 'CutNo_y', 'ProductionOrderID_y', 'CutQuantity_y',
            'MarkerID_y', 'ProductionOrderCode_y', 'SaleOrderID_y',
            'StyleTemplateID_y', 'IsFollowOperationSequence_y', 'SaleOrderCode_y',
            'Customer_y', 'OrderQuantity_y', 'StyleTemplateCode_y', 'MarkerCode_y',
            'MarkerMapping_y'], axis=1)

    piece_wise_scan_table_denorm.rename(
        {"CreatedAt_x": "CreatedAt", "UpdatedAt_x": "UpdatedAt", 'PieceID_x': 'PieceID',
         'PieceNumber_x': 'PieceNumber', 'BundleCode_x': 'BundleCode',
         'BundleQuantity_x': 'BundleQuantity', 'ScannedQuantity_x': 'ScannedQuantity',
            'RemainingQuantity_x': 'RemainingQuantity',
         'CutJobID_x': 'CutJobID', 'CutNo_x': 'CutNo', 'ProductionOrderID_x': "ProductionOrderID",
            'CutQuantity_x': 'CutQuantity',
         'MarkerID_x': 'MarkerID', 'ProductionOrderCode_x': 'ProductionOrderCode',
            'SaleOrderID_x': 'SaleOrderID',
         'StyleTemplateID_x': 'StyleTemplateID', 'IsFollowOperationSequence_x': 'IsFollowOperationSequence',
            'SaleOrderCode_x': 'SaleOrderCode',
         'Customer_x': 'Customer', 'OrderQuantity_x': 'OrderQuantity', 'StyleTemplateCode_x': 'StyleTemplateCode',
            'MarkerCode_x': 'MarkerCode',
         'MarkerMapping_x': 'MarkerMapping', 'IsMachineDown_x': 'IsMachineDown', 'BundleID_x': 'BundleID', 'PieceWiseGroupID_x': 'PieceWiseGroupID',
            'GroupName_x': 'GroupName'}, axis=1, inplace=True)

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

    operation_table_denorm = (
        operation_table.merge(section_table, how="left", on="SectionID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )

    operation_table_denorm.rename(
        {'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    tag_table_denorm = (
        tag_table.merge(cut_report_table_denorm, how="left", on="BundleID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )

    tag_table_denorm.rename(
        {'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    user_table_denorm = (
        user_table.merge(line_table, how="left", on="LineID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )
    user_table_denorm.rename(
        {'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    user_table_denorm = (
        user_table_denorm.merge(section_table, how="left", on="SectionID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )
    user_table_denorm.rename(
        {'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    userpermission_table_denorm = (
        userpermission_table.merge(module_table, how="left", on="ModuleID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )
    userpermission_table_denorm.rename(
        {'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    userpermission_table_denorm = (
        userpermission_table_denorm.merge(
            user_table_denorm, how="left", on="UserID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )
    userpermission_table_denorm.rename(
        {'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    line_layout_table_denorm = (
        line_layout_table.merge(line_table, how="left", on="LineID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )

    line_layout_table_denorm.rename(
        {'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    line_layout_table_denorm = (
        line_layout_table_denorm.merge(
            production_order_table_denorm, how="left", on="ProductionOrderID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )

    line_layout_table_denorm.rename(
        {'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    machine_down_time_table_denorm = (
        machine_down_time_table.merge(
            machine_table_denorm, how="left", on="MachineID")
        .drop(["CreatedAt_y", "UpdatedAt_y"], axis=1)
    )

    machine_down_time_table_denorm.rename(
        {'CreatedAt_x': 'CreatedAt', 'UpdatedAt_x': 'UpdatedAt'}, axis=1, inplace=True)

    # BULK INSERT

    myinsert('line', line_table, 50000, 1000000)

    # NEW TABLE
    myinsert('box', box_table)

    # NEW TABLE
    myinsert('line_layout', line_layout_table_denorm)

    myinsert('module', module_table, 50000, 1000000)
    myinsert('userpermission', userpermission_table_denorm, 50000, 1000000)

    myinsert('worker', worker_table, 50000, 1000000)
    myinsert('machine_type', machine_type_table, 50000, 1000000)
    myinsert('machine', machine_table_denorm, 50000, 1000000)

    # NEW TABLE
    myinsert("machine_down_time", machine_down_time_table_denorm)

    myinsert('sale_order', sale_order_table, 50000, 1000000)

    myinsert('section', section_table, 50000, 1000000)
    myinsert('user', user_table_denorm, 50000, 1000000)
    myinsert('operation', operation_table_denorm, 50000, 1000000)

    myinsert('worker_scan', worker_scan_table_denorm, 50000, 1000000)
    myinsert('style_template', style_template_table, 50000, 1000000)

    myinsert('style_bulletin', style_bulletin_table_denorm, 50000, 1000000)
    myinsert('production_order', production_order_table_denorm, 50000, 1000000)
    myinsert('marker', marker_table_denorm, 50000, 1000000)

    myinsert('cut_job', cut_job_table_denorm, 50000, 1000000)
    myinsert('cut_report', cut_report_table_denorm, 50000, 1000000)

    # NEW TABLE
    myinsert('scan_group', scan_group_table)
    myinsert('tag', tag_table_denorm, 50000, 1000000)

    myinsert('scan', scan_table_denorm, 50000, 1000000)

    # NEW TABLE
    myinsert('piece_wise_group', piece_wise_group_table_denorm)

    myinsert('piece_wise_scan', piece_wise_scan_table_denorm, 50000, 1000000)
    myinsert('piece_wise_cut_report',
             piece_wise_cut_report_table_denorm, 50000, 1000000)
    return {"status": "all data inserted"}
# --------------------------------------------------------------------------
# UPDATE FUNCTION

# --------------------------------------------------------------------------
# CREATING CSV FILE FOR ROW COUNTS


def mysql_to_dataframe():
    if os.path.exists("./dataframe_mysql.csv") == False:
        data_mysql = {"line": [mysqlRowcount("line")],
                      "module": [mysqlRowcount("module")],
                      "userpermission": [mysqlRowcount("userpermission")],
                      "worker": [mysqlRowcount("worker")],
                      "machine_type": [mysqlRowcount("machine_type")],
                      "machine": [mysqlRowcount("machine")],
                      "sale_order": [mysqlRowcount("sale_order")],
                      "section": [mysqlRowcount("section")],
                      "user": [mysqlRowcount("user")],
                      "operation": [mysqlRowcount("operation")],
                      "worker_scan": [mysqlRowcount("worker_scan")],
                      "style_template": [mysqlRowcount("style_template")],
                      "style_bulletin": [mysqlRowcount("style_bulletin")],
                      "production_order": [mysqlRowcount("production_order")],
                      "marker": [mysqlRowcount("marker")],
                      "cut_job": [mysqlRowcount("cut_job")],
                      "cut_report": [mysqlRowcount("cut_report")],
                      "tag": [mysqlRowcount("tag")],
                      "scan": [mysqlRowcount("scan")],
                      "piece_wise_scan": [mysqlRowcount("piece_wise_scan")],
                      "piece_wise_cut_report": [mysqlRowcount("piece_wise_cut_report")],

                      "line_layout": [mysqlRowcount("line_layout")],
                      "scan_group": [mysqlRowcount("scan_group")],
                      "box": [mysqlRowcount("box")],
                      "machine_down_time": [mysqlRowcount("machine_down_time")],
                      "piece_wise_group": [mysqlRowcount("piece_wise_group")]}
        mysql_df = pd.DataFrame(data_mysql)
    else:
        mysql_df = pd.read_csv("./dataframe_mysql.csv", index_col=[0])

    row = {"timestamp": pd.Timestamp.now(), "line": mysqlRowcount("line"),
           "module": mysqlRowcount("module"),
           "userpermission": mysqlRowcount("userpermission"),
           "worker": mysqlRowcount("worker"),
           "machine_type": mysqlRowcount("machine_type"),
           "machine": mysqlRowcount("machine"),
           "sale_order": mysqlRowcount("sale_order"),
           "section": mysqlRowcount("section"),
           "user": mysqlRowcount("user"),
           "operation": mysqlRowcount("operation"),
           "worker_scan": mysqlRowcount("worker_scan"),
           "style_template": mysqlRowcount("style_template"),
           "style_bulletin": mysqlRowcount("style_bulletin"),
           "production_order": mysqlRowcount("production_order"),
           "marker": mysqlRowcount("marker"),
           "cut_job": mysqlRowcount("cut_job"),
           "cut_report": mysqlRowcount("cut_report"),
           "tag": mysqlRowcount("tag"),
           "scan": mysqlRowcount("scan"),
           "piece_wise_scan": mysqlRowcount("piece_wise_scan"),
           "piece_wise_cut_report": mysqlRowcount("piece_wise_cut_report"),

           "line_layout": [mysqlRowcount("line_layout")],
           "scan_group": [mysqlRowcount("scan_group")],
           "box": [mysqlRowcount("box")],
           "machine_down_time": [mysqlRowcount("machine_down_time")],
           "piece_wise_group": [mysqlRowcount("piece_wise_group")]}
    row = pd.Series(row)

    mysql_df = mysql_df.append(row, ignore_index=True)
    tmp_mysql = './dataframe_mysql.csv'
    mysql_df.to_csv(tmp_mysql)
    return {"Status": "mysql dataframe created/updated."}


def postgres_to_dataframe():
    if os.path.exists("./dataframe_postgres.csv") == False:
        data_postgres = {
            "line": [postgresRowcount("line")],
            "module": [postgresRowcount("module")],
            "userpermission": [postgresRowcount("userpermission")],
            "worker": [postgresRowcount("worker")],
            "machine_type": [postgresRowcount("machine_type")],
            "machine": [postgresRowcount("machine")],
            "sale_order": [postgresRowcount("sale_order")],
            "section": [postgresRowcount("section")],
            "user": [postgresRowcount("user")],
            "operation": [postgresRowcount("operation")],
            "worker_scan": [postgresRowcount("worker_scan")],
            "style_template": [postgresRowcount("style_template")],
            "style_bulletin": [postgresRowcount("style_bulletin")],
            "production_order": [postgresRowcount("production_order")],
            "marker": [postgresRowcount("marker")],
            "cut_job": [postgresRowcount("cut_job")],
            "cut_report": [postgresRowcount("cut_report")],
            "tag": [postgresRowcount("tag")],
            "scan": [postgresRowcount("scan")],
            "piece_wise_scan": [postgresRowcount("piece_wise_scan")],
            "piece_wise_cut_report": [postgresRowcount("piece_wise_cut_report")],

            "line_layout": [postgresRowcount("line_layout")],
            "scan_group": [postgresRowcount("scan_group")],
            "box": [postgresRowcount("box")],
            "machine_down_time": [postgresRowcount("machine_down_time")],
            "piece_wise_group": [postgresRowcount("piece_wise_group")]}
        postgres_df = pd.DataFrame(data_postgres)
    else:
        postgres_df = pd.read_csv("./dataframe_postgres.csv", index_col=[0])

    row = {"timestamp": pd.Timestamp.now(),
           "line": postgresRowcount("line"),
           "module": postgresRowcount("module"),
           "userpermission": postgresRowcount("userpermission"),
           "worker": postgresRowcount("worker"),
           "machine_type": postgresRowcount("machine_type"),
           "machine": postgresRowcount("machine"),
           "sale_order": postgresRowcount("sale_order"),
           "section": postgresRowcount("section"),
           "user": postgresRowcount("user"),
           "operation": postgresRowcount("operation"),
           "worker_scan": postgresRowcount("worker_scan"),
           "style_template": postgresRowcount("style_template"),
           "style_bulletin": postgresRowcount("style_bulletin"),
           "production_order": postgresRowcount("production_order"),
           "marker": postgresRowcount("marker"),
           "cut_job": postgresRowcount("cut_job"),
           "cut_report": postgresRowcount("cut_report"),
           "tag": postgresRowcount("tag"),
           "scan": postgresRowcount("scan"),
           "piece_wise_scan": postgresRowcount("piece_wise_scan"),
           "piece_wise_cut_report": postgresRowcount("piece_wise_cut_report"),

           "line_layout": [postgresRowcount("line_layout")],
           "scan_group": [postgresRowcount("scan_group")],
           "box": [postgresRowcount("box")],
           "machine_down_time": [postgresRowcount("machine_down_time")],
           "piece_wise_group": [postgresRowcount("piece_wise_group")]
           }
    row = pd.Series(row)

    postgres_df = postgres_df.append(row, ignore_index=True)
    tmp_postgres = './dataframe_postgres.csv'
    postgres_df.to_csv(tmp_postgres)
    return {"status": "postgres dataframe file created/updated."}


def create_csv_logic():

    mysql_to_dataframe()
    postgres_to_dataframe()
    return {'status': 'Dataframe files created/updated.'}

# --------------------------------------------------------------------------
