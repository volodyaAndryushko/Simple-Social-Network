from typing import List

from flask import g

from src.api.errors import PostNotFound
from src.models.post import Like, Post


def get_post_by_id(post_id: int) -> Post:
    post = g.session.query(Post).filter_by(id=post_id).first()
    if not post:
        raise PostNotFound
    return post


def get_likes(user_id: int = None, post_id: int = None) -> List[Like]:
    query = g.session.query(Like)
    if user_id:
        query = query.filter_by(liked_by_id=user_id)
    if post_id:
        query = query.filter_by(post_id=post_id)
    return query.all()
