from flask import Flask
from flask_migrate import Migrate
from routes.myblueprint import blueprint
from flask_sqlalchemy import SQLAlchemy
from pprint import PrettyPrinter
from config.config import Config

pp = PrettyPrinter(indent=2)

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# creating models

db.create_all()
db.session.commit()

db.init_app(app)
migrate = Migrate(app, db)

# migrate.init_app(app, db)

app.register_blueprint(blueprint)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
