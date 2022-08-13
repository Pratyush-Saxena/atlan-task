from dataclasses import field
from models import db, User, Form, Field, Response, ResponseData


def get_user_by_id(user_id):
    try:
        user = db.session.query(User).filter_by(id=user_id).first()
        if user:
            return user
        else:
            return None
    except Exception as e:
        print(e)
        return None


def get_form_response(form_id, user_id):
    try:
        response = (
            db.session.query(Response)
            .filter_by(form_id=form_id, user_id=user_id)
            .first()
        )
        if response:
            response_data = {}
            response_data["created_at"] = response.created_at
            response_data["user"] = get_user_by_id(response.user_id).email
            response_data["data"] = []
            fields = db.session.query(Field).filter_by(form_id=form_id).all()
            data = []
            for field in fields:
                resp_data = (
                    db.session.query(ResponseData)
                    .filter_by(response_id=response.id, field_id=field.id)
                    .first()
                )
                field_data = field.serialize()
                field_data["value"] = resp_data.serialize() if resp_data else None
                data.append(field_data)
            response_data["data"] = data
            return response_data
    except Exception as e:
        print(e)


def get_all_response(form_id):
    try:
        fields = db.session.query(Field).filter_by(form_id=form_id).all()
        data = []
        responses = (
            db.session.query(Response)
            .filter_by(form_id=form_id)
            .order_by(Response.created_at.desc())
            .all()
        )
        for response in responses:
            resp_data = {}
            resp_data["created_at"] = response.created_at
            resp_data["user"] = get_user_by_id(response.user_id).email
            resp_data["data"] = []
            for field in fields:
                resp = (
                    db.session.query(ResponseData)
                    .filter_by(response_id=response.id, field_id=field.id)
                    .first()
                )
                resp_data["data"].append(
                    {"field": field.serialize(), "value": resp.value if resp else None}
                )
            data.append(resp_data)
        return data
    except Exception as e:
        print(e)
        return None
