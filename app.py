from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import func
from flask_restful import Resource, Api
from flask_apispec.extension import FlaskApiSpec
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

import os

app = Flask(__name__)

api = Api(app)
docs = FlaskApiSpec(app)



app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(
    {
        "APISPEC_SPEC": APISpec(
            title="Collect API",
            version="v1",
            plugins=[MarshmallowPlugin()],
            openapi_version="2.0.0",
        ),
        "APISPEC_SWAGGER_URL": "/swagger/",  # URI to access API Doc JSON
        "APISPEC_SWAGGER_UI_URL": "/swagger-ui/",  # URI to access UI of API Doc
    }
)
app.config['SECRET_KEY'] = 'U19*nk12JGBjskHjd4sdfkgsdhkvkhgFlhjdsGlhwUEWV&^(7fsdfds='


from models import db
migrate = Migrate(app, db)


@app.route('/')
def index():
    return 'Hey the app is running!'

@app.route('/test_db')
def test_db():
    try:
        resp=db.session.query(func.current_timestamp()).all()[0]
        s=''
        for e in resp:
            s+=str(e)
        return s
    except Exception as e:
        return(str(e))

from collect.user import UserResource
from collect.forms import FormResource
from collect.fields import FieldResource
api.add_resource(UserResource, '/User')
api.add_resource(FormResource, '/Forms')
api.add_resource(FieldResource, '/Forms/Field')


docs.register(UserResource)
docs.register(FormResource)
docs.register(FieldResource)

from auth.routes import (
    login,
    token_verify,
    refresh_token,
)
docs.register(login)
docs.register(token_verify)
docs.register(refresh_token)

from collect.routes import (
    get_all_forms,
    get_complete_form,
    create_new_response,
    get_user_response,
    get_all_responses,
)
docs.register(get_all_forms)
docs.register(get_complete_form)
docs.register(create_new_response)
docs.register(get_user_response)
docs.register(get_all_responses)



if __name__ == '__main__':
    app.run(debug=True)