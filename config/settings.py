from dotenv import dotenv_values
from datetime import datetime, timezone
import os 

# Google API 
GMAIL_SCOPES: list = ["https://www.googleapis.com/auth/gmail.readonly"]
TOKEN_NAME: str = "token.json"
SECRET_NAME: str = "client_secret.json"
TRIM_CONTENT: int = 200

# Several options that will be used for testing
STRIP_OPT: list = [
        "full", # Full match comparison
        "left", # Prefix match comparison
        "right" # Suffix match comparison
    ]

SORT_OPT: list = [
        "None", # Don`t sort
        "Asc", # Ascending order option
        "Desc" # Descending order option
    ]

# What would be used to test
CHANNEL: list = [
        "rikaiai-features",
        "social"
    ]

# Text that will be used for testing
MSG_INPUT: list = [
        (0, "this is a test", 2, "English", ["Korean", "Japanese"], True), # Message Location, Message, Translation Count (0, 1, 2), Source Language, Target, and Translate
        (1, "this is the second", 2, "English", ["Korean", "Japanese"], False)
    ]

# Project Context
DIR_PATH: str = os.path.join(os.path.dirname(__file__), "..", "api")
DATE_FORMAT: str ="%a, %d %b %Y %H:%M:%S %z"
MIN_DATE: object = datetime.min.replace(tzinfo=timezone.utc)


# Get data from .env file as dictionary
CONFIG: dict = dotenv_values(".env")
USER: str = CONFIG["USER"]
EMAIL: str = CONFIG["GMAIL"]
PASSWORD: str = CONFIG["GMAIL_PASSWORD"]
SITE: str = CONFIG["STAGING_URL"]
WORKSPACE: str = CONFIG["STAGING_NAME"]
