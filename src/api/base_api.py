import logging
from datetime import datetime
from functools import wraps

from flask import make_response, request, g
from flask_restful import Resource
import jwt

from src.app_conf import CONFIG
from src.api.errors import TokenRequired, TokenExpired, UnknownTokenError
from src.constants import FAIL, SUCCESS
from src.managers.user import get_user_by_id

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def format_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except Exception as e:
            g.session.rollback()
            logger.error(e)
            raise e
        else:
            g.session.commit()

        message = SUCCESS
        if isinstance(response, tuple):
            data, status = response
            if 400 <= status <= 404:
                message = FAIL
        else:
            data, status = response, 200

        if isinstance(data, dict) and "message" in data:
            response_data = data
        else:
            response_data = {"message": message, "data": data}
        response_data.update(status=message)
        return make_response(response_data, status)
    return wrapper


class BaseApi(Resource):
    """Use this class for the endpoints with no auth is required"""
    method_decorators = [format_response]


class AuthBaseApi(BaseApi):
    """Use on the endpoints with required auth"""
    def __init__(self):
        super(AuthBaseApi, self).__init__()

        self.token = None
        if 'HTTP_AUTHORIZATION' in request.headers.environ:
            self.token = request.headers.environ['HTTP_AUTHORIZATION'].split(" ")[1]

        if not self.token:
            raise TokenRequired
        else:
            self.user_id = self.decode_auth_token()

    def decode_auth_token(self) -> str:
        try:
            payload = jwt.decode(self.token, CONFIG["SECRET_KEY"], algorithms=["HS256"])
            user_id = payload["sub"]
            user_obj = get_user_by_id(user_id, return_as_dto=False)
            user_obj.last_request_time = datetime.utcnow()
            return user_id
        except jwt.ExpiredSignatureError:
            raise TokenExpired
        except Exception:
            raise UnknownTokenError


class WelcomeUser(BaseApi):
    @staticmethod
    def get():
        response = {"message": "Welcome to the Simple Social Network API!"}
        return response
