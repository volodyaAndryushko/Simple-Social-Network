import logging
import requests
from json import load
from random import randint, choice
from string import ascii_lowercase
from typing import List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s]: %(message)s')

SSN_BASE_URL = "http://0.0.0.0:5001"


def load_config():
    file_name = "bot_config.json"
    with open(file_name, "r") as conf:
        return load(conf)


def create_user():
    username = ''.join(choice(ascii_lowercase) for i in range(10))
    res = requests.post(SSN_BASE_URL + "/sign-up", json={"email": f"{username}@gmail.com", "password": "qwerty"})
    user_data = res.json().get("user")
    if not user_data:
        logging.error("User has not been created due to: " + str(res.json()))
        return
    logging.info(f"user created:\tuser_id: {user_data['id']}\temail: {user_data['email']}")
    return user_data


def create_post(index: int, access_token: str):
    res = requests.post(
        SSN_BASE_URL + "/posts",
        json={"title": f"My new post {index}", "content": "Lorem ipsum..."},
        headers={"Authorization": "Bearer " + access_token},
    )
    post_data = res.json().get("post")
    if not post_data:
        logging.error("Post has not been created")
        return
    logging.info(f"post created:\t post_data: {post_data}")
    return post_data


def create_like(post_ids: List[int], access_token: str):
    post_index = randint(0, len(post_ids) - 1)
    res = requests.post(
        SSN_BASE_URL + f"/posts/{post_ids[post_index]}/like",
        headers={"Authorization": "Bearer " + access_token}
    )
    msg = res.json().get("message")
    if not msg:
        logging.error("Like has not been created")
        return
    logging.info(msg)
    return msg


def start():
    config = load_config()
    number_of_users = config["number_of_users"]
    post_ids = []
    for _ in range(number_of_users):
        user_data = create_user()
        if not user_data:
            continue

        number_of_posts = randint(0, config["max_posts_per_user"])
        for post_i in range(number_of_posts):
            post_data = create_post(post_i, user_data["access_token"])
            post_ids.append(post_data["id"])

        number_of_likes = randint(0, config["max_likes_per_user"])
        for like_i in range(number_of_likes):
            create_like(post_ids, user_data["access_token"])


if __name__ == "__main__":
    logging.info("Starting the bot...")
    start()
