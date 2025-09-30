# import logging
# import os

# from dotenv import load_dotenv

# # load environment variable from .env file
# load_dotenv(os.getenv("ENV_FILE", ".env"))

# ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
# # redis
# REDIS_HOST = os.getenv("REDIS_HOST")

# logger = logging.getLogger(__name__)

import os
from dotenv import load_dotenv

load_dotenv()

# Twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Paths
PDF_DIR = os.getenv("PDF_DIR", "manuals/")
INDEX_DIR = os.getenv("INDEX_DIR", "vectorstore/")

