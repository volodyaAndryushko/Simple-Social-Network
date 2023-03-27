from typing import Dict

from flask import g

from src.models.post import Post


def create_post(author_id: int, post_data: Dict[str, str]) -> Post:
    new_post = Post(author_id=author_id, **post_data)
    g.session.add(new_post)
    g.session.flush()
    return new_post
