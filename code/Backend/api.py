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
    def post(self):
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

    def get(self):
        all_tickets = Tickets.query.all()
        res = []
        for ticket in all_tickets:
            res.append({
                'ticket_id': ticket.ticket_id,
                'user_id': ticket.users.first().id,
                'title': ticket.title,
                'description': ticket.description,
                'upvotes': ticket.upvotes,
                'status': ticket.status
            })
        return jsonify(res), 200

class ticketid_api:
    def put(self, ticket_id):
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

    def get(self, ticket_id):
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
        current_ticket = Tickets.query.filter(Tickets.ticket_id == ticket_id ).first()
        if not current_ticket:
            return 404
        current_ticket.delete()
        db.session.commit()
        return '', 204

class Votes_api:
    def put(self):
        upvote_data = request.get_json()
        
        curr_ticket = Tickets.query.filter(Tickets.ticket_id == upvote_data.ticket_id).first()
        upvoted = upvotes.query.filter(upvotes.id == current_user.id).filter(upvotes.ticket_id == upvote_data.ticket_id).first()
        
        if upvoted:
            return DefaultError(status_code=409,desc="The post has already upvoted by the current user")
        
        curr_ticket.upvotes = Tickets.upvotes +1
        user_upvote_rec = upvotes(id=current_user.id, ticket_id = curr_ticket.ticket_id)
        
        db.session.add(user_upvote_rec)
        db.session.commit()
        
        return '', 200

    def get(self):
        limit = request.args.get('limit', default=10, type=int)
        
        top_tickets = Tickets.query.order_by(Tickets.upvotes.desc()).limit(limit).all()
        
        res = []
        for ticket in top_tickets:
            res.append({
                'ticket_id': ticket.ticket_id,
                'user_id': ticket.users.first().id,
                'title': ticket.title,
                'description': ticket.description,
                'upvotes': ticket.upvotes,
                'status': ticket.status
            })
        return jsonify(res), 200

class ticketresolve_api:
    def post(self, ticket_id):
        response = request.get_json().response
        
        ticket = Tickets.query.filter(Tickets.ticket_id == ticket_id).first()
        ticket_responded = ticket.update({'response':response})
        
        db.session.commit()

        return '', 200
    
    def put(self, ticket_id):
        return self.post(ticket_id)

class faqs_api:
    def get():
        return faqs.query.all(), 200

    def post():
        faq_data = request.get_json()
        
        new_faq = faqs(question = faq_data.question, answer = faq_data.answer)
        
        db.session.add(new_faq)
        db.session.commit()

        return '', 201

class faqid_api:
    def get(f_id):
        return faqs.query.filter(faqs.f_id == f_id).first(), 200

    def put(f_id):
        faq_data = request.get_json()
        
        curr_faq = faqs.query.filter(faqs.f_id == f_id).first()
        
        if not curr_faq:
            return 404
        updated_faq = curr_faq.update({'question':faq_data.question,
                                       'answer':faq_data.answer})
        db.session.commit()
        return '',200
    
    def delete(f_id):
        
        curr_faq = faqs.query.filter(faqs.f_id == f_id).first()
        if not curr_faq:
            return 404
        curr_faq.delete()
        
        db.session.commit()
        
        return '', 204