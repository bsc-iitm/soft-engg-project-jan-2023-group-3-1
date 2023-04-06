import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api
from Backend.database import db
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from Backend.models import User,Role
from Backend.config import *

current_dir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config.from_object(LocalDevelopmentConfig)
db.init_app(app)
api = Api(app)
app.app_context().push()

CORS(app, resources={r'/*': {'origins': '*'}})

user_datastore =  SQLAlchemySessionUserDatastore(db.session,User,Role)

security = Security(app, datastore=user_datastore)

from Backend.controllers import *

from Backend.api import *

api.add_resource(tickets_api,'/tickets')
api.add_resource(ticketid_api,'/<int:ticket_id>')
api.add_resource(Votes_api,'/tickets/upvote')
api.add_resource(ticketresolve_api, '/tickets/<int:ticket_id>/answer')

if __name__ == "__main__":
    app.run(debug = True)