import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api
from Backend.database import db
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from Backend.models import *
from Backend.config import *

current_dir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(current_dir, 'database.sqlite3')
app.config.from_object(LocalDevelopmentConfig)
db.init_app(app)
api = Api(app)
app.app_context().push()

CORS(app, resources={r'/*': {'origins': '*'}})

user_datastore =  SQLAlchemySessionUserDatastore(db.session)

security = Security(app,user_datastore)

from Backend.controllers import *

from Backend.api import *


if __name__ == "__main__":
    app.run(debug = True)