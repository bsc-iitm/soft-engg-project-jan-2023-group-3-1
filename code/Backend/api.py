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
        res = curr_user.as_dict()
        res['role'] = curr_user.roles[0].name
        return make_response(jsonify(res), 200)

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
    def get(self):
        all_tickets = Tickets.query.all()
        res = []
        for ticket in all_tickets:
            temp = ticket.as_dict()
            temp['user'] = ticket.users[0].as_dict()
            if ticket.status == 'closed':
                staff = User.query.filter(resolvedby.ticket_id == ticket.ticket_id).filter(resolvedby.id == User.id).first()
                temp['staff'] = staff.as_dict()
            res.append(temp)
        return make_response(jsonify(res),200)

class ticketid_api(Resource):
    @auth_token_required
    def put(self, ticket_id):
        ticket_data = request.get_json()
        curr_ticket = Tickets.query.filter(Tickets.ticket_id == ticket_id)
        
        if not curr_ticket.first():
            return make_response('ticket with given id not found',404)
        
        if curr_ticket.first().status != 'open':
            return make_response('The ticket is not open and cannot be updated',405)
        
        if current_user.id != curr_ticket.first().users[0].id:
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
        
        res = curr_ticket.as_dict()
        res['user'] = curr_ticket.users[0].as_dict()
        if curr_ticket.status == 'closed':
            staff = User.query.filter(resolvedby.ticket_id == curr_ticket.ticket_id).filter(resolvedby.id == User.id).first()
            res['staff'] = staff.as_dict()
        return make_response(jsonify(res), 200)

    @auth_token_required
    def delete(self, ticket_id):
        current_ticket = Tickets.query.filter(Tickets.ticket_id == ticket_id ).first()
        if not current_ticket:
            return make_response('ticket with given id not found',404)
        db.session.delete(current_ticket)
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
            db.session.delete(upvoted)
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
            temp = ticket.as_dict()
            temp['user'] = ticket.users[0].as_dict()
            res.append(temp)
        return make_response(jsonify(res), 200)

class ticketresolve_api(Resource):
    @auth_token_required
    def post(self, ticket_id):
        response = request.get_json()['response']
        
        ticket = Tickets.query.filter(Tickets.ticket_id == ticket_id).first()
        ticket.response = response
        ticket.status = 'closed'
        ticket.date_closed = currtime()
        
        if resolvedby.query.filter(resolvedby.ticket_id == ticket.ticket_id).first():
            db.session.commit()
            return make_response('Response updated successfully',200)
        
        resolved_rec = resolvedby(ticket_id = ticket.ticket_id, id= current_user.id)
        
        db.session.add(resolved_rec)
        db.session.commit()

        return make_response('tciket successfully resolved',200)

class faqs_api(Resource):
    @auth_token_required
    def get(self):
        return make_response([faq.as_dict() for faq in faqs.query.all()], 200)

    @auth_token_required
    def post(self):
        faq_data = request.get_json()
        
        new_faq = faqs(question = faq_data['question'], answer = faq_data['answer'])
        
        db.session.add(new_faq)
        db.session.commit()

        return make_response('faq added successfuly',201)

class faqid_api(Resource):
    @auth_token_required
    def get(self,f_id):
        curr_faq = faqs.query.filter(faqs.f_id == f_id).first()
        if not curr_faq:
            return make_response('ticket not found', 404)
        return make_response(curr_faq.as_dict(), 200)

    @auth_token_required
    def put(self,f_id):
        faq_data = request.get_json()
        
        curr_faq = faqs.query.filter(faqs.f_id == f_id)
        
        if not curr_faq.first():
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
        
        db.session.delete(curr_faq)
        
        db.session.commit()
        
        return make_response('deleted successfully',204)
