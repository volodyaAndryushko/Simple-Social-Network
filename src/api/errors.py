from werkzeug.exceptions import HTTPException

from src.constants import FAIL


class ValidationError(HTTPException):
    code = 400
    data = {"message": "Validation error.", "error": "validation_error", "result": FAIL}

    def __init__(self, errors):
        super().__init__()
        self.data.update(errors=errors)


class InvalidCredentials(HTTPException):
    code = 401
    data = {"message": "Incorrect credentials.", "error": "invalid_credentials", "result": FAIL}


class EmailAlreadyTaken(HTTPException):
    code = 400
    data = {"message": "Email already taken.", "error": "email_already_taken", "result": FAIL}


class TokenRequired(HTTPException):
    code = 401
    data = {"message": "Token required.", "error": "token_required", "result": FAIL}


class TokenExpired(HTTPException):
    code = 401
    data = {"message": "Token expired.", "error": "token_expired", "result": FAIL}


class UnknownTokenError(HTTPException):
    code = 401
    data = {"message": "Unknown token error.", "error": "unknown_token_error", "result": FAIL}


class UserNotFound(HTTPException):
    code = 404
    data = {"message": "User not found.", "error": "user_not_found", "result": FAIL}


class ServiceUnavailable(HTTPException):
    code = 503
    data = {"message": "Service temporarily unavailable.", "error": "service_down", "result": FAIL}
