from src.api.base_api import AuthBaseApi
from src.api.errors import ValidationError
from src.managers import post as post_service


class Likes(AuthBaseApi):
    @staticmethod
    def validate_post_id(post_id: str):
        if not post_id or not post_id.isdigit():
            raise ValidationError("Not a valid post_id")

    def post(self, post_id):
        self.validate_post_id(post_id)
        new_like = post_service.add_like_to_post(self.user_id, int(post_id))
        return {"message": f"{new_like} successfully created."}, 201

    def delete(self, post_id):
        self.validate_post_id(post_id)
        post_service.remove_likes_from_post(self.user_id, int(post_id))
        return {"message": f"Likes on post #{post_id} by User #{self.user_id} where deleted"}, 200
