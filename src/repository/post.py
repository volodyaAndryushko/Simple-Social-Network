from datetime import datetime
from typing import List

from flask import g

from src.api.errors import PostNotFound
from src.models.post import Like, Post


def get_post_by_id(post_id: int) -> Post:
    post = g.session.query(Post).filter_by(id=post_id).first()
    if not post:
        raise PostNotFound
    return post


def get_likes(
    user_id: int = None, post_id: int = None, date_from: datetime = None, date_to: datetime = None
) -> List[Like]:
    query = g.session.query(Like)
    if user_id:
        query = query.filter(Like.liked_by_id == user_id)
    if post_id:
        query = query.filter(Like.post_id == post_id)
    if date_from:
        query = query.filter(Like.created_time >= date_from)
    if date_to:
        query = query.filter(Like.created_time <= date_to)
    return query.all()
