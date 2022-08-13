from flask_restful import Resource
from flask_apispec.views import MethodResource
from flask_apispec import use_kwargs, marshal_with
from auth.utils import token_required
from models import Field, db, Form
from marshmallow import fields
from .schema import FieldSchema


class FieldResource(MethodResource, Resource):
    
        @use_kwargs(FieldSchema)
        @token_required
        def post(self, **kwargs):
            try:
                if db.session.query(Form).filter_by(id=kwargs['form_id'],user_id=kwargs['user'].id).first():
                    field = Field(name=kwargs.get('name'), form_id=(kwargs.get('form_id')), description=kwargs.get('description'), type=(kwargs.get('type')).upper(), mandate=kwargs.get('mandate'), upper_limit=kwargs.get('upper_limit'), lower_limit=kwargs.get('lower_limit'), options=kwargs.get('options'), question=kwargs.get('question'))
                    db.session.add(field)
                    db.session.commit()
                    return {'message': 'Field created successfully', 'data': field.serialize()}, 201
                return {'message': 'You are not authorized to create this field'}, 401
            except Exception as e:
                print(e)
                return {'message': 'Something Went Wrong!'}, 500
        
        @use_kwargs(FieldSchema)
        @token_required
        def put(self,**kwargs):
            try:
                if db.session.query(Form).filter_by(id=kwargs['form_id'],user_id=kwargs['user'].id).first():
                    field = db.session.query(Field).filter_by(id=kwargs['id'],form_id=kwargs['form_id']).first()
                    if field:
                        field.name = kwargs.get('name')
                        field.description = kwargs.get('description')
                        field.type = (kwargs.get('type')).upper()
                        field.mandate = kwargs.get('mandate')
                        field.upper_limit = kwargs.get('upper_limit')
                        field.lower_limit = kwargs.get('lower_limit')
                        field.options = kwargs.get('options')
                        field.question = kwargs.get('question')
                        db.session.commit()
                        return {'message': 'Field updated successfully', 'data': field.serialize()}, 200
                    else:
                        return {'message': 'Field not found'}, 404
                return {'message': 'You are not authorized to update this field'}, 401
            except Exception as e:
                print(e)
                return {'message': 'Something Went Wrong!'}, 500
        
        @use_kwargs({'id': fields.Int(required=True)})
        @token_required
        def delete(self, **kwargs):
            try:
                if db.session.query(Form).filter_by(id=kwargs['form_id'],user_id=kwargs['user'].id).first():
                    field = db.session.query(Field).filter_by(id=kwargs['id']).first()
                    if field:
                        db.session.delete(field)
                        db.session.commit()
                        return {'message': 'Field deleted successfully'}, 200
                    else:
                        return {'message': 'Field not found'}, 404
                return {'message': 'You are not authorized to delete this field'}, 401
            except Exception as e:
                print(e)
                return {'message': 'Something Went Wrong!'}, 500

