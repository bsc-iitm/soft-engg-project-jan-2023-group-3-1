import json
import datetime , calendar , os, string,random
from distutils.log import Log
from sqlalchemy import extract,func
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask,request,render_template,redirect, url_for,jsonify, make_response
from flask import current_app as app
from .models import *
from .api import currtime
from flask_security import auth_token_required
from flask_login import login_required,current_user
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
    return redirect('http://localhost:8082/')

@app.route('/roleselect', methods=['GET','POST'])
@login_required
def role_select():
    if request.method == 'GET':
        if current_user.roles:
            return "Role already assigned"
        roles = Role.query.all()
        return render_template("role_select.html",roles=roles)
    
    if request.method == 'POST':
        role = request.form.get('role')
        curr_id = current_user.id
        adding_relation = user_role(id = curr_id,role_id=role)
        db.session.add(adding_relation)
        db.session.commit()
        return redirect('http://localhost:8082/')