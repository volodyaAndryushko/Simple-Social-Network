import logging

from src import app


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


application = app.create_app()

if __name__ == "__main__":
    logger.info("Starting the API ...")
    application.run(port=5001, host="0.0.0.0")
