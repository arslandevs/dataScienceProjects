from services.user_service import insert_logic, create_logic
# import test
from services.user_service import create_csv_logic
from services.update_service import update_logic


def index():
    return {'status': 'OK',
            'localhost:5000/create': 'Create tables in postgres database',
            'localhost:5000/insert': 'Insert data in postgres database tables(Inserttable)',
            'localhost:5000/create_csv': 'create csv files with row counts of the databases(mysql and postrges).',
            'localhost:5000/update':'update the values'}


def create():

    return create_logic()

# insert data into table.


def insert():

    return insert_logic()


def update():
    return update_logic()


def create_csv():

    return create_csv_logic()
