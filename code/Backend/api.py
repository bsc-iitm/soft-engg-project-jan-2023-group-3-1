from flask import make_response, request,session, url_for
import os
import pandas as pd
from flask_restful import Resource, Api, marshal_with, fields
from .database import db 
from .models import *
from werkzeug.exceptions import HTTPException
import json
from flask_security import auth_token_required
from flask import current_app as app


class DefaultError(HTTPException):
    def __init__(self, status_code, desc):
        self.response = make_response('', status_code)
        self.description = "<p>"+desc+"</p>"

class Success(HTTPException):
    def __init__(self, status_code, msg):
        self.response = make_response(msg, status_code)

class BError(HTTPException):
    def __init__(self, status_code, errorcode, errormsg):
        message = {
  "error_code": errorcode,
  "error_message": errormsg
}
        self.response = make_response(json.dumps(message), status_code)

