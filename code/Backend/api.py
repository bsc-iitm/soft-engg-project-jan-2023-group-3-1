from flask import make_response, request, jsonify
import datetime
from .database import db 
from .models import *
from flask_restful import Resource
from werkzeug.exceptions import HTTPException
from flask_security import auth_token_required,login_user
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

class user_api(Resource):
    @auth_token_required
    def post(self):
        creds = request.get_json()
        curr_user = User.query.filter(User.email == creds['email']).first()
        login_user(curr_user)
        return make_response(jsonify(curr_user.as_dict()), 200)

class tickets_api(Resource):
    @auth_token_required
    def post(self):
        try:
            ticket_data = request.get_json()
            new_ticket = Tickets(
                        date_created = currtime(),
                        last_modified = currtime(),
                        title = ticket_data['title'],
                        description = ticket_data['description']
                        )
            db.session.add(new_ticket)
            db.session.commit()
            ticket_id = new_ticket.ticket_id
            user_ticket = tickets_users(
                        ticket_id = ticket_id,
                        id = current_user.id
            )
            db.session.add(user_ticket)
            db.session.commit()
        except:
            return make_response('Could no add the ticket',400)
        return make_response(f'Added ticket with id-{ticket_id}', 201)

    @auth_token_required
    def get(self,useronly, status, limit):
        tickets = Tickets.query()
        
        if useronly:
            if current_user.roles[0].name == 'Student':
                tickets = tickets.filter(Tickets.ticket_id == tickets_users.ticket_id)\
                                .filter(tickets_users.id == current_user.id)
            else:
                tickets = tickets.filter(Tickets.ticket_id == resolvedby.ticket_id)\
                                .filter(resolvedby.id == current_user.id)
        if status:
            tickets = tickets.filter(Tickets.status == status)
            
        tickets = tickets.limit(limit)
        
        res = []
        for ticket in tickets:
            res.append({
                'ticket_id': ticket.ticket_id,
                'user_id': ticket.users[0].id,
                'title': ticket.title,
                'description': ticket.description,
                'upvotes': ticket.upvotes,
                'status': ticket.status
            })
        return make_response(jsonify(res),200)
    
    @auth_token_required
    def get(self):
        all_tickets = Tickets.query.all()
        res = []
        for ticket in all_tickets:
            res.append({
                'ticket_id': ticket.ticket_id,
                'user_id': ticket.users[0].id,
                'title': ticket.title,
                'description': ticket.description,
                'upvotes': ticket.upvotes,
                'status': ticket.status
            })
        return make_response(jsonify(res),200)

class ticketid_api(Resource):
    @auth_token_required
    def put(self, ticket_id):
        ticket_data = request.get_json()
        curr_ticket = Tickets.query.filter(Tickets.ticket_id == ticket_id).first()
        
        if not curr_ticket:
            return make_response('ticket with given id not found',404)
        
        if curr_ticket.status != 'open':
            return make_response('The ticket is not open and cannot be updated',405)
        
        if current_user.id != curr_ticket.users.first().id:
            return make_response('You are not authorised to update the ticket of other users',403)
        
        updated_ticket = curr_ticket.update({
                        'title': ticket_data['title'],
                        'description': ticket_data['description'],
                        'last_modified': currtime()
        })
        db.session.commit()
        
        return make_response('ticket created succesfully', 200)

    @auth_token_required
    def get(self, ticket_id):
        curr_ticket = Tickets.query.filter(Tickets.ticket_id == ticket_id).first()

        if not curr_ticket:
            return make_response('Not found',404)
        
        return make_response(jsonify({
            'ticket_id': ticket_id,
            'user_id': curr_ticket.users.first().id,
            'title': curr_ticket.title,
            'description': curr_ticket.description,
            'upvotes': curr_ticket.upvotes,
            'status': curr_ticket.status
        }), 200)

    @auth_token_required
    def delete(ticket_id):
        current_ticket = Tickets.query.filter(Tickets.ticket_id == ticket_id ).first()
        if not current_ticket:
            return make_response('ticket with given id not found',404)
        current_ticket.delete()
        db.session.commit()
        return make_response('deleted successfully',204)

class Votes_api(Resource):
    @auth_token_required
    def put(self):
        upvote_data = request.get_json()
        
        curr_ticket = Tickets.query.filter(Tickets.ticket_id == upvote_data['ticket_id']).first()
        upvoted = upvotes.query.filter(upvotes.id == current_user.id).filter(upvotes.ticket_id == upvote_data['ticket_id']).first()
        
        if upvoted:
            curr_ticket.upvotes = Tickets.upvotes -1
            upvoted.delete()
            db.session.commit()
            return make_response("post upvote removed successfully",200)
        
        curr_ticket.upvotes = Tickets.upvotes +1
        user_upvote_rec = upvotes(id=current_user.id, ticket_id = curr_ticket.ticket_id)
        
        db.session.add(user_upvote_rec)
        db.session.commit()
        
        return make_response('post upvoted successfully',200)

    @auth_token_required
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
        return make_response(jsonify(res), 200)

class ticketresolve_api(Resource):
    @auth_token_required
    def post(self, ticket_id):
        response = request.get_json()['response']
        
        ticket = Tickets.query.filter(Tickets.ticket_id == ticket_id).first()
        ticket_responded = ticket.update({'response':response, 'status':'closed'})
        resolved_rec = resolvedby(ticket_id = ticket.ticket_id, id= current_user.id)
        
        db.session.add(resolved_rec)
        db.session.commit()

        return make_response('',200)
    
    @auth_token_required
    def put(self, ticket_id):
        return self.post(ticket_id)

class faqs_api(Resource):
    @auth_token_required
    def get(self):
        return make_response(faqs.query.all(), 200)

    @auth_token_required
    def post(self):
        faq_data = request.get_json()
        
        new_faq = faqs(question = faq_data['question'], answer = faq_data['answer'])
        
        db.session.add(new_faq)
        db.session.commit()

        return make_response('',201)

class faqid_api(Resource):
    @auth_token_required
    def get(self,f_id):
        return make_response(faqs.query.filter(faqs.f_id == f_id).first(), 200)

    @auth_token_required
    def put(self,f_id):
        faq_data = request.get_json()
        
        curr_faq = faqs.query.filter(faqs.f_id == f_id).first()
        
        if not curr_faq:
            return make_response('FAQ with given id not found',404)
        updated_faq = curr_faq.update({'question':faq_data['question'],
                                       'answer':faq_data['answer']})
        db.session.commit()
        return make_response('',200)
    
    @auth_token_required
    def delete(self,f_id):
        
        curr_faq = faqs.query.filter(faqs.f_id == f_id).first()
        if not curr_faq:
            return 404
        curr_faq.delete()
        
        db.session.commit()
        
        return make_response('deleted successfully',204)
