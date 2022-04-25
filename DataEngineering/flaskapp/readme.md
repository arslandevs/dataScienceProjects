# ETL(Extract-transform-load)
In this article I will show how I'm performing ETL to extract data from mysql database and doing the necessary transformation to load the transformed data to postgres database.

To extract data I'm using following tools and technologies:
- python
- pandas 
- sqlalchemy
- flask
- flask_sqlalchemy
- flask_migrate
- pprint
- psycopg2

## 1. **Extracting data from MYSQL**
To get the data I'm using a sql command to get all the query set.

For instance:
```
machine = session_mysql.execute("select * from machine").all()
```

Next create a dataframe of all the input data. 

```
machine_table = pd.DataFrame()
```

It is important to define each column datatype to make the inserting data type consistent with the target database columns data types.

```
machine_table.astype()
```

## 2. **Transforming data**
To apply transformation, in our case we've to denormalize a database use the merge() function to get the left join of the two target tables.

```
machine_table.merge()
```

## 3. **Loading data to POSTGRES**
For inserting I'm using psycopg **copy_from()**  method that insert from the select pandas dataframe to the target table.

I've made a function **`myinsert()`** that takes four arguments **'table'** data to be inserted in, **'df'** as the transformed dataframe, **batch_size** to insert data if data is greater than **'data_threshold'**.  
In the first insertion when the postgres database is empty it will insert all the data in postgres.
After you run again it will insert only the new records if any are in the mysql database to be inserted in postgres.

For instance:
```
myinsert('machine',machine_table_denorm,50000,1000000)
```

## 4. **Using Flask app**

| Environment Variable | Description |
| :--- |:--- |
| `set FLASK_ENV=development` | Tell that we are on development environment. |
| `set FLASK_APP=app` | Tells the server to detect our app. |
| `flask run` | Start our app. |