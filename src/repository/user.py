from typing import Optional

from flask import g

from src.models.user import User


def get_user_by_id(user_id: int) -> Optional[User]:
    return g.session.query(User).filter_by(id=user_id).first()


def get_user_by_email(email: str) -> Optional[User]:
    return g.session.query(User).filter_by(email=email).first()
