from flask_restful import Resource
from flask_apispec.views import MethodResource
from flask_apispec import use_kwargs, marshal_with
from collect.schema import UserSchema
from marshmallow import fields
from models import User, db


class UserResource(MethodResource, Resource):
    @use_kwargs(UserSchema)
    def post(self, email,password):
        try:
            user = User.query.filter_by(email=email).first()
            if user:
                return {'message': 'User already exists'}, 400
            new_user=User(email=email,password=password)
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'User created successfully'}, 201
        except Exception as e:
            print(e)
            return {'message': 'Something Went Wrong!'}, 500
    
    @use_kwargs(UserSchema)
    def delete(self, email,password):
        try:
            user = User.query.filter_by(email=email).first()
            if user and user.password==password:
                db.session.delete(user)
                db.session.commit()
                return {'message': 'User deleted successfully'}, 200
            return {'message': 'Invalid Credentials'}, 401
        except Exception as e:
            print(e)
            return {'message': 'Something Went Wrong!'}, 500


    


        


