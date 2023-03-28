from typing import Dict

from flask import g

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
