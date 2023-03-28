from flask import make_response, request,session, url_for, jsonify, FLask
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

# Creating a new ticket
@app.route('/tickets', methods=['POST'])
def create_ticket():
    ticket_data = request.get_json()
    # Your code for creating a new ticket goes here
    # ...
    # Return the ticket information
    return jsonify({
        'id': 'ticket_id',
        'student_id': ticket_data['student_id'],
        'title': ticket_data['title'],
        'description': ticket_data['description'],
        'upvotes': 0,
        'status': 'open'
    }), 201

# Getting all tickets
@app.route('/tickets', methods=['GET'])
def get_tickets():
    # Your code for getting all tickets goes here
    # ...
    # Return the list of tickets
    return jsonify([
        {
            'id': 'ticket_id',
            'student_id': 'student_id',
            'title': 'ticket_title',
            'description': 'ticket_description',
            'upvotes': 0,
            'status': 'open'
        }
    ]), 200

# Updating ticket status
@app.route('/<ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    ticket_data = request.get_json()
    # Your code for updating the ticket status goes here
    # ...
    # Return the updated ticket information
    return jsonify({
        'id': ticket_id,
        'student_id': 'student_id',
        'title': 'ticket_title',
        'description': 'ticket_description',
        'upvotes': 0,
        'status': ticket_data['status']
    }), 200

# Getting ticket details
@app.route('/<ticket_id>', methods=['GET'])
def get_ticket_details(ticket_id):
    # Your code for getting the ticket details goes here
    # ...
    # Return the ticket details
    return jsonify({
        'id': ticket_id,
        'student_id': 'student_id',
        'title': 'ticket_title',
        'description': 'ticket_description',
        'upvotes': 0,
        'status': 'open'
    }), 200

# Deleting a ticket
@app.route('/<ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    # Your code for deleting the ticket goes here
    # ...
    return '', 204

# Upvoting a ticket
@app.route('/tickets/upvote', methods=['PUT'])
def upvote_ticket():
    upvote_data = request.get_json()
    # Your code for upvoting the ticket goes here
    # ...
    return '', 200

# Getting most upvoted tickets
@app.route('/tickets/upvote', methods=['GET'])
def get_most_upvoted_tickets():
    limit = request.args.get('limit', default=10, type=int)
    # Your code for getting the most upvoted tickets goes here
    # ...
    # Return the list of most upvoted tickets
    return jsonify([
        {
            'id': 'ticket_id',
            'student_id': 'student_id',
            'title': 'ticket_title',
            'description': 'ticket_description',
            'upvotes': 0,
            'status': 'open'
        }
    ]), 200


