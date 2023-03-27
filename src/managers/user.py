from typing import Dict

from flask import g

from src.api.errors import InvalidCredentials, EmailAlreadyTaken, UserNotFound
from src.models.user import User
from src.repository import user as user_repo


def create_new_user(user_data: Dict[str, str]) -> User:
    if user_repo.get_user_by_email(email=user_data["email"]):
        raise EmailAlreadyTaken
    new_user = User(email=user_data["email"])
    new_user.hash_password(user_data["password"])
    g.session.add(new_user)
    g.session.flush()
    return new_user


def login_user(user_data: Dict[str, str]) -> User:
    user = user_repo.get_user_by_email(email=user_data["email"])
    if not user or not user.verify_password(user_data["password"]):
        raise InvalidCredentials
    return user


def get_user_by_id(user_id: int) -> User:
    if user := user_repo.get_user_by_id(user_id):
        return user
    raise UserNotFound
