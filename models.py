from email.policy import default
from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

db=SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User {self.email}>'

class Form(db.Model):
    __tablename__ = 'forms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    published = db.Column(db.Boolean,default=False)
    author = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='SET NULL'), nullable=True)

    def __init__(self, name, author, published=False):
        self.name = name
        self.author = author
        self.published = published



class Field(db.Model):
    __tablename__ = 'fields'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True,default='Text')
    description = db.Column(db.Text(), nullable=True)
    question = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=False, default='TEXT', server_default='TEXT')
    form_id = db.Column(db.Integer, db.ForeignKey('forms.id',ondelete='CASCADE'), nullable=False)
    mandate = db.Column(db.Boolean,default=False)
    upper_limit = db.Column(db.Integer, nullable=True, default=None)
    lower_limit = db.Column(db.Integer, nullable=True,default=None)
    options = db.Column(db.ARRAY(db.String), nullable=True, default=None)


    def __init__(self, name, description, question, type, form_id,  upper_limit, lower_limit,mandate=True, options=None):
        self.name = name
        self.description = description
        self.question = question
        self.type = type if type in ['TEXT','NUMBER','CHOICE','FILE'] else 'TEXT'
        self.mandate = mandate
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit
        self.options = options
        self.form_id = form_id



class Response(db.Model):
    __tablename__ = 'responses'
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('forms.id',ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    def __init__(self, form_id, user_id):
        self.form_id = form_id
        self.user_id = user_id

class ResponseData(db.Model):
    __tablename__ = 'responsedata'
    id = db.Column(db.Integer, primary_key=True)
    response_id = db.Column(db.Integer, db.ForeignKey('responses.id',ondelete='CASCADE'), nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id',ondelete='CASCADE'), nullable=False)
    value = db.Column(db.Text, nullable=True)

    def __init__(self, response_id, field_id, value):
        self.response_id = response_id
        self.field_id = field_id
        self.value = value

