from datetime import datetime, timedelta
from random import choice
from string import ascii_uppercase, digits

import jwt
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import Column, DateTime, Integer, String, Text

from src.app_conf import CONFIG
from src.app import Base


class User(Base):
    __tablename__ = "user"

    id = Column("id", Integer, primary_key=True)
    email = Column("email", String(100), nullable=False, unique=True)
    password_salt = Column("password_salt", String(30), nullable=True)
    password_hash = Column("password_hash", Text, nullable=True)
    created_time = Column("created_time", DateTime, default=datetime.utcnow)
    last_login_time = Column("last_login_time", DateTime)
    last_request_time = Column("last_request_time", DateTime)

    def __repr__(self):
        return f"<User #{self.id} - {self.email}>"

    def hash_password(self, password: str):
        self.password_salt = _get_random_str(15)
        self.password_hash = pwd_context.encrypt(f"{password}:{self.password_salt}")

    def verify_password(self, password: str):
        return pwd_context.verify(f"{password}:{self.password_salt}", self.password_hash)

    def encode_auth_token(self):
        payload = {
            "exp": datetime.utcnow() + timedelta(seconds=CONFIG["JWT_EXPIRES_IN"]),
            "iat": datetime.utcnow(),
            "sub": self.id,
        }
        token = jwt.encode(payload, CONFIG["SECRET_KEY"], algorithm="HS256")
        self.last_login_time = datetime.utcnow()
        self.last_request_time = datetime.utcnow()
        return token

    def as_dict(self, generate_new_token: bool = False):
        # todo: move to DTO class
        user_dict = {
            "id": self.id,
            "email": self.email,
            "created_time": self.created_time,
            "last_login_time": self.last_login_time,
            "last_request_time": self.last_request_time,
        }
        user_dict.update(access_token=self.encode_auth_token()) if generate_new_token else None
        return user_dict


def _get_random_str(size=6, chars=ascii_uppercase + digits):
    return ''.join(choice(chars) for _ in range(size))
