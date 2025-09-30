

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

