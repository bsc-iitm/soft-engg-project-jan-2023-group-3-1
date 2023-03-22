import json
import datetime , calendar , os, string,random
from distutils.log import Log
from sqlalchemy import extract,func
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask,request,render_template,redirect, url_for,jsonify,session
from flask import current_app as app
from .models import *
import flask_login
from flask_login import login_required
from flask_caching import Cache
cache = Cache(app)

# code to prevent the app from loading cached images/data and always load only the supplied data.
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)
def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route('/',methods=['GET','POST'])
def homepage():
    return redirect('http://192.168.1.5:8080/')