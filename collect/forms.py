from flask_restful import Resource
from flask_apispec.views import MethodResource
from flask_apispec import use_kwargs, marshal_with
from auth.utils import token_required,get_user_from_token
from models import Form, db
from marshmallow import fields

class FormResource(MethodResource, Resource):

    @use_kwargs({'name': fields.Str(required=True),'published': fields.Bool(required=True)})
    @token_required
    def post(self, **kwargs):
        try:
            form = Form(name=kwargs['name'], published=kwargs['published'],user_id=kwargs['user'].id)
            db.session.add(form)
            db.session.commit()
            return {'message': 'Form created successfully', 'data': form.serialize()}, 201
        except Exception as e:
            print(e)
            return {'message': 'Something Went Wrong!'}, 500
    
    @use_kwargs({'id': fields.Int(required=True)})
    @token_required
    def get(self, **kwargs):
        try:
            form = Form.query.filter_by(id=kwargs['id'],user_id=kwargs['user'].id).first()
            if form:
                return {'message': 'Form found', 'data': form.serialize()}, 200
            else:
                return {'message': 'Form not found'}, 404
        except Exception as e:
            print(e)
            return {'message': 'Something Went Wrong!'}, 500
    
    @use_kwargs({'id': fields.Int(required=True),'name': fields.Str(required=True),'published': fields.Bool(required=True)})
    @token_required
    def put(self, **kwargs):
        try:
            form = Form.query.filter_by(id=kwargs['id'],user_id=kwargs['user'].id).first()
            if form:
                form.name = kwargs['name']
                form.published = kwargs['published']
                db.session.commit()
                return {'message': 'Form updated successfully', 'data': form.serialize()}, 200
            else:
                return {'message': 'Form not found'}, 404
        except Exception as e:
            print(e)
            return {'message': 'Something Went Wrong!'}, 500
    
    @use_kwargs({'id': fields.Int(required=True)})
    @token_required
    def delete(self, **kwargs):
        try:
            form = Form.query.filter_by(id=kwargs['id'],user_id=kwargs['user'].id).first()
            if form:
                db.session.delete(form)
                db.session.commit()
                return {'message': 'Form deleted successfully'}, 200
            else:
                return {'message': 'Form not found'}, 404
        except Exception as e:
            print(e)
            return {'message': 'Something Went Wrong!'}, 500

