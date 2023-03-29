from src.api.base_api import AuthBaseApi
from src.managers import user as user_service


class Me(AuthBaseApi):
    def get(self):
        user = user_service.get_user_by_id(self.user_id)
        return {"user": user.as_dict(), "message": "User info sent"}, 200
