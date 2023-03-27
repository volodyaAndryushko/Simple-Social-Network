import time

Base = ...
Session = ...


def create_app():
    import logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    from flask import Flask
    application = Flask(__name__)

    from src.app_conf import CONFIG
    application.secret_key = CONFIG["SECRET_KEY"]

    init_db()
    from flask_restful import Api

    api = Api(application)

    application.config["JWT_TOKEN_LOCATION"] = ["headers"]

    from src.api.encoder import JSONEncoder
    application.json_encoder = JSONEncoder

    from flask import g, request

    @application.before_request
    def before_request():
        g.start = time.time()
        g.session = Session()

    @application.after_request
    def after_request(response):
        if g.session is not None:
            g.session.close()
            diff = time.time() - g.start
            logger.info(
                f"[Request time] Path : {request.method} {request.full_path} | Time : {diff}s "
                f"| Status : {response.status}"
            )
            return response
        return response

    from src.api.init import register_api
    register_api(api)

    return application


def init_db():
    import logging
    from time import sleep

    from alembic.config import Config
    from alembic import command
    from sqlalchemy import create_engine
    from sqlalchemy.exc import OperationalError as SQLAlchemyConnectionError
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy_utils import create_database, database_exists

    from src.app_conf import CONFIG
    from src.api.errors import ServiceUnavailable

    db_url = CONFIG["DATABASE_URL"]
    logger = logging.getLogger(__name__)

    retries = 10
    while retries > 0:
        try:
            if not database_exists(db_url):
                create_database(db_url)
            break
        except SQLAlchemyConnectionError:
            if retries == 0:
                raise ServiceUnavailable("PostgreSQL connection failed")
            retries -= 1
            logger.error(f"Can not connect the database server. Retries left: {retries}]\nRetrying...")
            sleep(2)

    engine = create_engine(db_url, pool_pre_ping=True)
    global Base
    Base = declarative_base()

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    global Session
    Session = sessionmaker(bind=engine)
    return engine, Session
