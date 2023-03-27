from flask import request

from src.api.base_api import AuthBaseApi
from src.api.errors import ValidationError
from src.api.posts.schemas.posts import post_schema
from src.managers import post as post_service


class Posts(AuthBaseApi):
    def post(self):
        form_data = request.get_json()
        errors = post_schema.validate(form_data)
        if errors:
            raise ValidationError(errors)

        new_post = post_service.create_post(self.user_id, form_data)
        return {"post": new_post.as_dict(), "message": "Post successfully created."}, 201
