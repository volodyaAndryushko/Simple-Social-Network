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


class TokenRequired(HTTPException):
    code = 401
    data = {"message": "Token required.", "error": "token_required", "result": FAIL}


class ServiceUnavailable(HTTPException):
    code = 503
    data = {"message": "Service temporarily unavailable.", "error": "service_down", "result": FAIL}
