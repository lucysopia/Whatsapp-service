import logging
import os

from dotenv import load_dotenv

# load environment variable from .env file
load_dotenv(os.getenv("ENV_FILE", ".env"))

ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
# redis
REDIS_HOST = os.getenv("REDIS_HOST")

logger = logging.getLogger(__name__)
