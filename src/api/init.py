from src.api.auth.auth import UserSignUp, UserLogin
from src.api.base_api import WelcomeUser
from src.api.posts.posts import Posts
from src.api.posts.likes import Likes
from src.api.analytics.analytics import Analytics


def register_api(api):
    api.add_resource(WelcomeUser, "/")
    api.add_resource(UserSignUp, "/sign-up")
    api.add_resource(UserLogin, "/sign-in")
    api.add_resource(Posts, "/posts")
    api.add_resource(Likes, "/posts/<post_id>/like")
    api.add_resource(Analytics, "/analytics")
