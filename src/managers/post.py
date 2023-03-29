from collections import defaultdict
from datetime import datetime
from typing import Dict

from flask import g

from src.constants import DATE_FORMAT
from src.models.post import Like, Post
from src.repository import post as post_repo


def create_post(author_id: int, post_data: Dict[str, str]) -> Post:
    new_post = Post(author_id=author_id, **post_data)
    g.session.add(new_post)
    g.session.flush()
    return new_post


def add_like_to_post(user_id: int, post_id: int) -> Like:
    post_repo.get_post_by_id(post_id)
    new_like = Like(post_id=post_id, liked_by_id=user_id)
    g.session.add(new_like)
    g.session.flush()
    return new_like


def remove_likes_from_post(user_id: int, post_id: int):
    for like in post_repo.get_likes(user_id=user_id, post_id=post_id):
        g.session.delete(like)


def get_analytics(date_from: str = None, date_to: str = None) -> Dict[str, int]:
    date_from = datetime.strptime(date_from, DATE_FORMAT) if date_from else None
    date_to = datetime.strptime(date_to, DATE_FORMAT) if date_to else None

    res = defaultdict(int)
    for like in post_repo.get_likes(date_from=date_from, date_to=date_to):
        res[like.created_time.strftime(DATE_FORMAT)] += 1

    res.default_factory = None
    return res
