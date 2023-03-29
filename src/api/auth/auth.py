from flask import request

from src.api.auth.schemas.auth import user_auth_schema
from src.api.base_api import BaseApi
from src.api.errors import ValidationError
from src.managers import user as user_service


class UserSignUp(BaseApi):
    @staticmethod
    def post():
        form_data = request.get_json()
        errors = user_auth_schema.validate(form_data)
        if errors:
            raise ValidationError(errors)

        user = user_service.create_new_user(form_data)
        response = {"user": user.as_dict(), "message": "User created!"}
        return response, 201


class UserLogin(BaseApi):
    @staticmethod
    def post():
        form_data = request.get_json()
        errors = user_auth_schema.validate(form_data)
        if errors:
            raise ValidationError(errors)

        user = user_service.login_user(form_data)
        return {"user": user.as_dict(), "message": "User logged in."}
