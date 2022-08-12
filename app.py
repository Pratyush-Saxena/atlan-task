from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import func
from flask_restful import Resource, Api

import os

app = Flask(__name__)

api = Api(app)


app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db
migrate = Migrate(app, db)

from models import (
    User,
    Form,
    Field,
    Response,
    ResponseData,
)


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

if __name__ == '__main__':
    app.run(debug=True)