from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Union

from flask import g

from src.api.errors import InvalidCredentials, EmailAlreadyTaken, UserNotFound
from src.models.user import User
from src.repository import user as user_repo


@dataclass
class UserDTO:
    id: int = None
    email: str = None
    access_token: str = None
    created_time: datetime = None
    last_login_time: datetime = None
    last_request_time: datetime = None

    def as_dict(self):
        res = dict(
            id=self.id,
            email=self.email,
            created_time=self.created_time,
            last_login_time=self.last_login_time,
            last_request_time=self.last_request_time,
        )
        res.update(access_token=self.access_token) if self.access_token else None
        return res


def _build_user_dto(user: User, token: str = None):
    return UserDTO(
        id=user.id,
        email=user.email,
        created_time=user.created_time,
        last_login_time=user.last_login_time,
        last_request_time=user.last_request_time,
        access_token=token,
    )


def create_new_user(user_data: Dict[str, str]) -> UserDTO:
    if user_repo.get_user_by_email(email=user_data["email"]):
        raise EmailAlreadyTaken

    new_user = User(email=user_data["email"])
    new_user.hash_password(user_data["password"])
    g.session.add(new_user)
    g.session.flush()
    token = new_user.encode_auth_token()

    user_dto = _build_user_dto(new_user, token)
    return user_dto


def login_user(user_data: Dict[str, str]) -> UserDTO:
    user = user_repo.get_user_by_email(email=user_data["email"])
    if not user or not user.verify_password(user_data["password"]):
        raise InvalidCredentials

    token = user.encode_auth_token()
    user_dto = _build_user_dto(user, token)
    return user_dto


def get_user_by_id(user_id: int, return_as_dto: bool = True) -> Union[User, UserDTO]:
    if user := user_repo.get_user_by_id(user_id):
        return _build_user_dto(user) if return_as_dto else user
    raise UserNotFound
