from flask import request

from src.api.analytics.schemas.analytics import analytics_schema
from src.api.base_api import AuthBaseApi
from src.api.errors import ValidationError
from src.managers import post as post_service


class Analytics(AuthBaseApi):
    def get(self):
        errors = analytics_schema.validate(request.args)
        if errors:
            raise ValidationError(errors)

        analytics = post_service.get_analytics(**request.args)
        return {"analytics": analytics, "message": "Analytics sent"}, 200
