from flask import make_response, request,session, url_for, jsonify, FLask
import os, datetime
import pandas as pd
from flask_restful import Resource, Api, marshal_with, fields
from .database import db 
from .models import *
from werkzeug.exceptions import HTTPException
import json
from flask_security import auth_token_required
from flask_login import current_user
from flask import current_app as app

def currtime():
    return datetime.datetime.now()

class DefaultError(HTTPException):
    def __init__(self, status_code, desc):
        self.response = make_response('', status_code)
        self.description = "<p>"+desc+"</p>"

class Success(HTTPException):
    def __init__(self, status_code, msg):
        self.response = make_response(msg, status_code)

class tickets_api:
    def post():
        try:
            ticket_data = request.get_json()
            new_ticket = Tickets(
                        date_created = currtime(),
                        last_modified = currtime(),
                        title = ticket_data.title,
                        description = ticket_data.description
                        )
            db.session.add(new_ticket)
            
            ticket_id = new_ticket.ticket_id
            user_ticket = tickets_users(
                        ticket_id = ticket_id,
                        id = current_user.id
            )
            db.session.add(user_ticket)
            db.session.commit()
        except:
            return 400
        return jsonify({
            'ticket_id': ticket_id,
            'user_id': current_user.id,
            'title': ticket_data['title'],
            'description': ticket_data['description'],
            'upvotes': 0,
            'status': 'open'
        }), 201

    def get():
        all_tickets = Tickets.query.all()
        res = []
        for ticket in all_tickets:
            res.append({
                'ticket_id': ticket.ticket_id,
                'student_id': ticket.users.first().id,
                'title': ticket.title,
                'description': ticket.description,
                'upvotes': ticket.upvotes,
                'status': ticket.status
            })
        return jsonify(res), 200

class ticketid_api:
    def put(ticket_id):
        ticket_data = request.get_json()
        curr_ticket = Tickets.query.filter(Tickets.ticket_id == ticket_id).first()
        
        if not curr_ticket:
            return 404
        
        if curr_ticket.status != 'open':
            return DefaultError(status_code=405,desc='The ticket is not open and cannot be updated')
        
        if current_user.id != curr_ticket.users.first().id:
            return DefaultError(status_code=403, desc='You are not authorised to update the ticket of other users')
        
        updated_ticket = curr_ticket.update({
                        'title': ticket_data.title,
                        'description': ticket_data.description,
                        'last_modified': currtime()
        })
        db.session.commit()
        
        return jsonify({
            'ticket_id': ticket_id,
            'user_id': current_user.id,
            'title': ticket_data.title,
            'description': ticket_data.desc,
            'upvotes': curr_ticket.upvotes,
            'status': curr_ticket.status
        }), 200

    def get(ticket_id):
        curr_ticket = Tickets.query.filter(Tickets.ticket_id == ticket_id).first()

        if not curr_ticket:
            return 404
        
        return jsonify({
            'ticket_id': ticket_id,
            'user_id': curr_ticket.users.first().id,
            'title': curr_ticket.title,
            'description': curr_ticket.description,
            'upvotes': curr_ticket.upvotes,
            'status': curr_ticket.status
        }), 200

    def delete(ticket_id):
        current_ticket = Tickets.query.filter(Tickets.ticket_id == ticket_id )
        if not current_ticket:
            return 404
        current_ticket.delete()
        db.session.commit()
        return '', 204

class Votes_api:
    def put():
        upvote_data = request.get_json()
        # Your code for upvoting the ticket goes here
        # ...
        return '', 200

    def get():
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


