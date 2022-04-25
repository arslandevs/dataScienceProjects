import pandas as pd
from mysql.connector import connect

conn = connect(user='root', passwd='...', host='...', db='...')
mycursor = conn.cursor()

dataframe = pd.read_sql("Select * from test1", conn)
dataframe.reset_index(drop=True).drop(columns="id")

mycursor.execute(
    "INSERT INTO test1 (id, fname,	lname,	age) VALUES (6,'saad', 'ramzan', 24)")
conn.commit()

# TODO: Using the Where statement

mycursor.execute("select * from test1 where age >= %s",
                 (20,))  # thid %s will prevent sql injection


result = mycursor.fetchall()

for i in result:
    print(i)


# TODO: Using the count statement(tells the rows)

mycursor.execute("select count(*) from table1")
result = mycursor.fetchall()

for i in result:
    print(i)


# TODO: Using order by, offset, limit:

mycursor.execute("Select * from table1 order by salary Desc  limit 1 offset 0")
result = mycursor.fetchall()
for i in result:
    print(i)

# TODO: Using order by, offset, limit:

mycursor.execute("Select * from table1")
result = mycursor.fetchall()
for i in result:
    print(i)
