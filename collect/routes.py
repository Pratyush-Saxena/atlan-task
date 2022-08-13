from models import db, User, Form, Field, Response, ResponseData
from webargs import fields
from flask_apispec import use_kwargs, marshal_with
from auth.utils import token_required
from app import app
from .utils import get_form_response, get_all_response
from plugins.googlesheet import GS

@app.route('/form/get_all_forms', methods=['GET'])
@token_required
def get_all_forms(**kwargs):
    try:
        forms = db.session.query(Form).filter_by(user_id=kwargs['user'].id).all()
        if forms:
            return {'message': 'Forms found', 'data': [form.serialize() for form in forms]}, 200
        else:
            return {'message': 'Forms not found'}, 404
    except Exception as e:
        print(e)
        return {'message': 'Something Went Wrong!'}, 500


@app.route('/form/get_complete_form/<int:form_id>', methods=['GET'])
@token_required
def get_complete_form(form_id, **kwargs):
    try:
        form = db.session.query(Form).filter_by(id=form_id, user_id=kwargs['user'].id).first()
        if form:
            fields = db.session.query(Field).filter_by(form_id=form_id).all()
            if fields:
                return {'message': 'Form found', 'data': {'form': form.serialize(), 'fields': [field.serialize() for field in fields]}}, 200
            else:
                return {'message': 'Form not found'}, 404
        else:
            return {'message': 'Form not found'}, 404
    except Exception as e:
        print(e)
        return {'message': 'Something Went Wrong!'}, 500

@app.route('/form/new_response/<int:form_id>', methods=['POST'])
@use_kwargs({'data': fields.Dict(required=True)})
@token_required
def create_new_response(form_id, **kwargs):
    try:
        form = db.session.query(Form).filter_by(id=form_id).first()
        if form:
            if db.session.query(Response).filter_by(form_id=form_id, user_id=kwargs['user'].id).first():
                return {'message': 'Response already exists'}, 409

            fields = db.session.query(Field).filter_by(form_id=form_id).all()
            new_response= Response(form_id=form_id, user_id=kwargs['user'].id)
            db.session.add(new_response)
            db.session.flush()
            new_response
            data=kwargs['data']
            print
            for field in fields:
                if (not data.get(str(field.id))) and field['required']:
                    db.session.rollback()
                    return {'message': 'Missing required field'}, 400
                new_response_data=ResponseData(response_id=new_response.id, field_id=field.id, value=data.get(str(field.id)))
                db.session.add(new_response_data)
            db.session.commit()
            return {'message': 'Response created successfully', 'data': get_form_response(form_id, kwargs['user'].id)}, 201
        return {'message': 'Form not found'}, 404
    except Exception as e:
        db.session.rollback()
        print(e)
        return {'message': 'Something Went Wrong!'}, 500

@app.route('/form/get_user_response/<int:form_id>', methods=['GET'])
@token_required
def get_user_response(form_id, **kwargs):
    try:
        response = db.session.query(Response).filter_by(form_id=form_id, user_id=kwargs['user'].id).first()
        if response:
            return {'message': 'Response found', 'data': get_form_response(form_id, kwargs['user'].id)}, 200
        else:
            return {'message': 'Response not found'}, 404
    except Exception as e:
        print(e)
        return {'message': 'Something Went Wrong!'}, 500

@app.route('/form/get_all_responses/<int:form_id>', methods=['GET'])
@token_required
def get_all_responses(form_id, **kwargs):
    try:
        form=db.session.query(Form).filter_by(id=form_id, user_id=kwargs['user'].id).first()
        if form:
            resp=get_all_response(form_id)
            if resp:
                return {'message': 'Responses found', 'data': resp}, 200
            return {'message': 'No Response Found'}, 200
        return {'message': 'Form not found'}, 404
    except Exception as e:
        print(e)
        return {'message': 'Something Went Wrong!'}, 500

@app.route('/form/get_response_in_google_sheet/<int:form_id>', methods=['GET'])
@token_required
def get_response_in_google_sheet(form_id, **kwargs):
    try:
        form=db.session.query(Form).filter_by(id=form_id, user_id=kwargs['user'].id).first()
        if form:
            gs=GS()
            if gs.service:
                gsheet=gs.create_sheet(form.name)
                fields=db.session.query(Field).filter_by(form_id=form_id).all()
                field_names=([field.question for field in fields])
                values=[]
                values.append(field_names)
                for resp in db.session.query(Response).filter_by(form_id=form_id).all():
                    response=[]
                    for field in fields:
                        response.append(db.session.query(ResponseData).filter_by(response_id=resp.id, field_id=field.id).first().value)
                    values.append(response)
                gs.update_spreadsheet(gsheet['spreadsheetId'], values,'A1')
                return {'message': 'GoogleSheet Created', 'data': gsheet['spreadsheetUrl']}, 200
            return {'message': 'Error occured while creating sheet '}, 500
        return {'message': 'Form not found'}, 404
    except Exception as e:
        print(e)
        return {'message': 'Something Went Wrong!'}, 500


