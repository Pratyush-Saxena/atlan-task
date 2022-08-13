from models import db, User
from webargs import fields
from flask_apispec import use_kwargs, marshal_with
import jwt
from datetime import datetime, timedelta
from app import app
from auth.utils import verify_token

@app.route('/auth/login', methods=['POST'])
@use_kwargs({'email': fields.Str(required=True),'password': fields.Str(required=True)})
def login(**kwargs):
    try:
        user = User.query.filter_by(email=kwargs['email']).first()
        if user and user.password==kwargs['password']:
            payload = {'exp': datetime.utcnow() + timedelta(minutes=30),
                       'iat': datetime.utcnow(),
                       'sub': user.id}
            token = jwt.encode(payload, app.config['SECRET_KEY'])
            return {'token': token}, 200
        return {'message': 'Invalid Credentials'}, 401
    except Exception as e:
        print(str(e))
        return {'message': 'Something went wrong'}, 500

@app.route('/auth/verify_token', methods=['POST'])
@use_kwargs({'token': fields.Str(required=True)})
def token_verify(**kwargs):
    return verify_token(kwargs['token'])



@app.route('/auth/refresh_token', methods=['POST'])
@use_kwargs({'token': fields.Str(required=True)})
def refresh_token(**kwargs):
    try:
        payload = jwt.decode(algorithms=['HS256'],
                                key=app.config['SECRET_KEY'],
                                options={'verify_exp': True},
                                jwt=kwargs['token'])
        payload = {'exp': datetime.utcnow() + timedelta(minutes=30),
                'iat': datetime.utcnow(),
                'sub': payload['sub']}
        token = jwt.encode(payload, app.config['SECRET_KEY'])
        return {'token': token}, 200
    except jwt.ExpiredSignatureError:
        return {'message': 'Token Expired'}, 401
    except jwt.InvalidTokenError:
        return {'message': 'Invalid Token'}, 401
    except Exception as e:
        print(str(e))
        return {'message': 'Something went wrong'}, 500

    



