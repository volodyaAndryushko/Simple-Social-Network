from typing import Optional

from flask import g

from src.models.user import User


def get_user_by_email(email) -> Optional[User]:
    return g.session.query(User).filter_by(email=email).first()
