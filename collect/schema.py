from email import message
from typing import Any, Optional
from marshmallow import Schema, fields


class UserSchema(Schema):
    # name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class FieldSchema(Schema):
    id=fields.Int()
    name = fields.Str()
    form_id = fields.Int(required=True)
    description = fields.Str()
    type = fields.Str(required=True, validate=lambda x: x.upper() in ['TEXT','NUMBER','CHOICE','FILE'])
    mandate = fields.Bool()
    upper_limit = fields.Int()
    lower_limit = fields.Int()
    options = fields.List(fields.Str())
    question = fields.Str()



