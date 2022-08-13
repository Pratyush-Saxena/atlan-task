from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
from models import User, db


def verify_token(token):
    try:
        payload = jwt.decode(
            algorithms=["HS256"],
            key=current_app.config["SECRET_KEY"],
            options={"verify_exp": True},
            jwt=token,
        )
        return {"message": "Token Verified"}, 200
    except jwt.ExpiredSignatureError:
        return {"message": "Token Expired"}, 401
    except jwt.InvalidTokenError:
        return {"message": "Invalid Token"}, 401
    except Exception as e:
        print(str(e))
        return {"message": "Something went wrong"}, 500


def get_user_from_token(token):
    try:
        payload = jwt.decode(
            algorithms=["HS256"],
            key=current_app.config["SECRET_KEY"],
            options={"verify_exp": True},
            jwt=token,
        )
        user = User.query.filter_by(id=payload["sub"]).first()
        return user
    except Exception as e:
        print(str(e))
        return None


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get("Authorization"):
            return {"message": "Missing Authorization Header"}, 401
        token = request.headers.get("Authorization").split(" ")[1]
        response, status = verify_token(token)
        if status != 200:
            return response, status
        kwargs["user"] = get_user_from_token(token)
        return f(*args, **kwargs)

    return decorated_function
