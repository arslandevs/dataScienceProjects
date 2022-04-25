# Minimal Flask Application using MVC design pattern

<p align='center'>
<img src='https://github.com/SyedArsalanAmin/alpha/blob/master/static/images/mvc%20architecture.png?raw=true' alt='drawing' width='600' height='300'/>
</p>

## **Tools and Technologies**

<p float="left">
  <img src="https://www.vectorlogo.zone/logos/python/python-icon.svg" width='100'>
  <img src="https://flask.palletsprojects.com/en/2.0.x/_images/flask-logo.png" width="200"/>
  <img src="https://www.vectorlogo.zone/logos/mysql/mysql-ar21.svg" width="200" />
  <img src="https://flask-sqlalchemy.palletsprojects.com/en/2.x/_static/flask-sqlalchemy-logo.png" width="130" />
</p>

Below are the Tools and Technologies used:

- Python.
- Flask.
- Model View Controller (MVC).
- Mysql.
- Flask-sqlalchemy.

## **Introduction**

If are new to programming you maybe writing some code in a file and then you simply run it and boom your code is running! But that not the case when you make organized application with lot of features.

## What to do then?

A common practice is to always follow a software design pattern even if your application is small, in future if you want to add some features then it would be easier to add if your code is in MVC because your code will be more organized, maintainable, reusable and flexible.

## Why use these software design patterns?

If you do not follow these patterns probably you'll get stuck in some kind of problem that will tease you to progress. Like myself, when I started to learn backend development I got stuck in cyclic dependency problem. That slowed down my development process.
There are lot of software design patterns but for MVC it provide the idea of `seperation of concerns.`

## How this will help you?

I've implemented a simple flask application with mysql database using mvc design pattern. For using mysql database I've used flask-sqlalchemy package which is a popular ORM. ORM is a object relational mapper. It is a way to map the database tables to python objects. That makes it easier to work with the database.

> ### **"MVC architecture helps us to control the complexity of application by dividing it into three components i.e. model, view and controller"**
>
> [Source](https://crimsonpublishers.com/prsp/pdf/PRSP.000505.pdf)

## File tree structure

Lets take a look at the file structure:

```
📦src
 ┣ 📂controllers
 ┃ ┗ 📜machineController.py
 ┣ 📂models
 ┃ ┗ 📜machine.py
 ┣ 📂routes
 ┃ ┗ 📜blueprint.py
 ┣ 📂services
 ┃ ┗ 📜user_service.py
 ┣ 📜app.py
 ┣ 📜config.py
 ┗ 📜data.json
```

## **Let's deep dive into this!**

We should have knowledge about how server requst and response works. When a user request a page from a particular server, it will recieve the request and in result sends a response to the user. The response could be html page.

One thing is important i'm explaining the mvc structure with flask app, code logic is not point of dicussion here!

## Routes:

First user visit a URL that will be redirected to the specific page. The router is the address to which the user will be redirected. For example, if user wants to visit home page then he will type `http://localhost:5000/machines` in the url bar.

```python
from flask import Blueprint
from controllers.machineController import index, create, insert

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/', methods=['GET'])(index)
blueprint.route('/create', methods=['GET'])(create)
blueprint.route('/insert', methods=['GET'])(insert)
```

We are using flask-REST API. You can also use FastApi. But for this one we are using flask one. So on hitting a specific endpoint a method will be called that is linked with that endpoint in our case it's `/machines` because we are using `url_prefix='/machines'.`

## **What is Blueprint?**

In simpe words they record each operation that is performed on the application. When flask generate a URL from an endpoint it will link the view function with blueprint.

## **Why use Blueprint?**

- We are using flask blueprints that a way through which we can factor an application into smaller pieces.
- We can register a blueprint on an application at a URL prefix.
- We can register multiple blueprints on an application.

Isn't that amazing!

## **Model**:

Models represent the data and its related logic. They are the core of the application. It will decide the data that is being transfered between the controller and other business logic.
For example in our case the controller is responsible for creating table(Inserttable) in mysql database.

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Creating the Inserttable for inserting data into the database


class Inserttable(db.Model):
    '''Data for ON/OFF should be dumped in this table.

    Table has below fields:
    id: Primary key
    machineid
    stateid
    speed
    statechange
    unixtime
    extras
    state'''

    __tablename__ = 'inserttable'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    machineid = db.Column(db.Integer, primary_key=False)
    stateid = db.Column(db.Integer, primary_key=False)
    speed = db.Column(db.Integer, nullable=False)
    statechange = db.Column(db.Integer, nullable=False)
    unixtime = db.Column(db.Integer, nullable=False)
    extras = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)

    # method used to represent a class's objects as a string
    def __repr__(self):
        return '<machineid %r>' % self.machineid

```

In the figure above you can see the illustration the only the model has access to the database. Models access database directly and and that data is being used by the controller and ultimately for the view to display.

## Controller:

Controller is like middle-man between view and models. They take input and talk directly to the model that will communicate with the database.

### **Logic part**

```
Here you can see that I'm reading data from the data.json and using the StateId int value's binary I decide what to set the state column to in MYSQL database table(inserttable). You can simply add some data in fields in the table instead of this logic.
```

```python
import json
from models.machine import Inserttable, db
from services.user_service import insert_logic, create_logic

def index():
    return {'status': 'OK',
            'localhost:5000/machines/create': 'Create table in mysql database',
            'localhost:5000/machines/insert': 'Insert data in mysql database table(Inserttable)'}

# here you can observe that the core logic are hidden from the application, which is good to 
def create():

    create_logic()


# insert data into table.
def insert():

    insert_logic()
```

Note:controller don't communicate directly with the database there is model between database and controller.

In the above code index, create and insert method talk to the model. The controller tells the model what to do. The model then communicates with the database and fetches data then comes the view part.

## Services(additional layer):

When your applications grows and more features are added to it, it is a better practice to separate the business logic from the application. A service layer adds an additional layer of abstraction between the application and the business logic. It has the core business logic.

You can think of it as worker. While controller is the manager that just handles what to do, services are the workers that do the actual work and return what is required by the api user. In summary:

- controller(manager): manages the work.
- services(worker): do the work.

```python
import json
from models.machine import Inserttable, db

def create_logic():
    try:
        # create tables if not exists.
        db.create_all()
        db.session.commit()
        return '==================TABLES CREATED=================='

    except Exception as e:
        print(e)
        return '==================TABLES NOT CREATED!!!=================='


def insert_logic():
    data = json.load(open("data.json", 'r'))  # reading file data.json
    for i, b in enumerate('{0:016b}'.format(data['StateId'])):
        if int(b) == 1:
            example = Inserttable(machineid=data["MachineId"], stateid=data["StateId"],
                                  speed=data["Speed"], statechange=data["StateChange"],
                                  unixtime=data["UnixTime"], extras=data["Extras"],
                                  state="ON")

            db.session.add(example)
            # db.session.commit()

        else:
            example = Inserttable(machineid=data["MachineId"], stateid=data["StateId"],
                                  speed=data["Speed"], statechange=data["StateChange"],
                                  unixtime=data["UnixTime"], extras=data["Extras"],
                                  state="OFF")

            db.session.add(example)
            # db.session.commit()
    return '==================DATA INSERTED=================='
    db.session.commit()
    # db.session.close()
```

## View:

Now the view is the part of the application that is responsible for displaying the data.
It can be a simple return string or a fully fledged html page with beautiful design.
I'm not implementting the view part in this tutorial just to show how to make a simple flask app with mvc structure.

## Config file:

This file contains cinfiguration for the database. For other database you can use different file configurations.

```python
import os

# Each Flask web application contains a secret key which used to sign session cookies for protection against cookie data tampering.
SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
# In my case it is, "F:\DataScience_Ai\hobby_projects\mvc_project\src"
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode, that will refresh the page when you make changes.
DEBUG = True

# Connect to the MYSQL database
SQLALCHEMY_DATABASE_URI = 'mysql://root:<your_password>@localhost/<your_database_name>'

# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False

```

## App file:

This is main file of the application. It has the modules which we created and then call that here. First we are creating app flask object, configuring and initializing the database.
Then you have to register the blueprint as discussed above. And finally running the application using `'flask run'` command in the terminal.

Flask app requires some environment variables to be set. These are as follows:
| Environment Variable | Description |
| :--- |:--- |
| `set FLASK_ENV=development` | Tell that we are on development environment. |
| `set FLASK_APP=app` | Tells the server to detect our app. |
| `flask run` | Start our app. |

```python
# Importing the necessary modules and libraries
from flask import Flask
from flask_migrate import Migrate
from routes.blueprint import blueprint
from models.machine import db


def create_app():
    app = Flask(__name__)  # flask app object
    app.config.from_object('config')  # Configuring from Python Files

    db.init_app(app)  # Initializing the database
    return app


app = create_app()  # Creating the app
# Registering the blueprint
app.register_blueprint(blueprint, url_prefix='/machines')
migrate = Migrate(app, db)  # Initializing the migration


if __name__ == '__main__':  # Running the app
    app.run(host='127.0.0.1', port=5000, debug=True)

```

## Running the app:

Below are the screenshots of the running app. You can see that the app is running on localhost:5000. When we hit on `machines/create` table(inserttable) is created and `machines/insert` insert the data in the database table.

<p float="left">
  <img src="https://github.com/SyedArsalanAmin/alpha/blob/master/static/images/screenshot1.png?raw=true" 
  width='400'>
  <img src="https://github.com/SyedArsalanAmin/alpha/blob/master/static/images/Screenshot2.png?raw=true" width="400"/>
  <img src="https://github.com/SyedArsalanAmin/alpha/blob/master/static/images/Screenshot5.png?raw=true" width="400" />
</p>

## Table and data:

Below you can see the table and data inserted in the database.

<p float="left">
  <img src="https://github.com/SyedArsalanAmin/alpha/blob/master/static/images/Screenshot3.png?raw=true" width="200" />
  <img src="https://github.com/SyedArsalanAmin/alpha/blob/master/static/images/Screenshot4.png?raw=true" width="400" />
</p>

## Conclusion:

In this tutorial we not only went through mvc but also implemented a simple flask application with mvc structure. You can make a flask application in a single file but for more sophisticated applications you have to make use of MVC structure.

We learned how blueprint works, what is the file structure and how does MVC works practically.

MVC has three layers:

## Model:

It communicates with the database.

## View:

It displays the data on the screen.

## Controller:

It is a interconnection between the model and the view part.

Hurrah ! 🥳 Now you know how to make a flask application with mvc structure. Go ahead implement it and make interesting applications. Please upvote and follow me and do share your thoughts and suggestions. 😀

Thanks for reading!

<!-- ![img](https://github.com/SyedArsalanAmin/alpha/blob/master/static/icons/appreciation.png?raw=true) -->

<p align='center'>
<img src='https://github.com/SyedArsalanAmin/alpha/blob/master/static/icons/appreciation.png?raw=true' alt='drawing' width='100'/>
</p>
