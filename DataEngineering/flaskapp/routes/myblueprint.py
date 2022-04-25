from crypt import methods
from flask import Blueprint
from controllers.mycontrol import index, create, insert
from controllers.mycontrol import update,create_csv

blueprint = Blueprint('blueprint', __name__)

blueprint.route('/', methods=['GET'])(index)
blueprint.route('/create', methods=['GET'])(create)
blueprint.route('/insert', methods=['GET'])(insert)
blueprint.route('/update', methods=['GET'])(update)
blueprint.route('/create_csv', methods=['GET'])(create_csv)