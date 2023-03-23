from .database import db
from flask_security import UserMixin,RoleMixin

class User(db.Model,UserMixin):
    __tablename__ = "Users"
    id = db.Column(db.Integer,nullable=False,unique=True, primary_key=True,autoincrement=True)
    username = db.Column(db.String)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    fs_uniquifier = db.Column(db.String,unique=True, nullable=False)
    active = db.Column(db.Boolean())
    
    roles= db.relationship('Roles',secondary="user_role",backref=db.backref('users',lazy='dynamic'))
    
    #This funcion will return a row in the query as a dictionary.
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# This is a secondary table linking the users to their roles.
class user_role(db.Model):
    __tablename__ = 'user_role'
    role_id = db.Column(db.Integer, db.ForeignKey('Roles.role_id'),primary_key=True, nullable=False)
    id = db.Column(db.Integer,db.ForeignKey('Users.id'),nullable=False,primary_key=True)

class Role(db.Model,RoleMixin):
    __tablename__ = 'Roles'
    role_id = db.Column(db.Integer,nullable=False,unique=True, primary_key=True)
    name = db.Column(db.String)
    Description = db.Column(db.String) 

class Tickets(db.Model):
    __tablename__ = "Tickets"
    ticket_id = db.Column(db.Integer,nullable=False, unique=True, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False)
    last_modified = db.Column(db.DateTime, nullable=False)
    date_closed = db.Column(db.DateTime)
    upvotes = db.Column(db.Integer, nullable=False, default=0)
    title = db.Column(db.String,nullable=False)
    description = db.Column(db.String,nullable=False)
    response = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False, default="open")
    
    users = db.relationship('User',secondary='tickets_users', backref=db.backref('tickets',lazy='dynamic'))
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# This is a secondary table linking the tickets with the users
class tickets_users(db.Model):
    __tablename__ = 'tickets_users'
    ticket_id = db.Column(db.Integer, db.ForeignKey('Tickets.ticket_id'),primary_key=True, nullable=False)
    id = db.Column(db.Integer,db.ForeignKey('Users.id'),nullable=False,primary_key=True)

class faqs(db.Model):
    __tablename__ = "faqs"
    f_id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)