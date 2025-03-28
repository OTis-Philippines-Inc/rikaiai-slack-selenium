from dotenv import dotenv_values
from datetime import datetime, timezone
import numpy as np
import os 

# Google API 
GMAIL_SCOPES: list = ["https://www.googleapis.com/auth/gmail.readonly"]
TOKEN_NAME: str = "token.json"
SECRET_NAME: str = "client_secret.json"
TRIM_CONTENT: int = 200

# Enums 
STRIP_OPT: object = np.array([
        "full", # Full match comparison
        "left", # Prefix match comparison
        "right" # Suffix match comparison
    ])

SORT_OPT: object = np.array([
        "None", # Don`t sort
        "Asc", # Ascending order option
        "Desc" # Descending order option
    ])

# What would be used to test
CHANNEL: object = np.array([
        "rikaiai-features",
        "social"
    ])

# Project Context
DIR_PATH: str = os.path.join(os.path.dirname(__file__), "..", "api")
DATE_FORMAT: str ="%a, %d %b %Y %H:%M:%S %z"
MIN_DATE: object = datetime.min.replace(tzinfo=timezone.utc)
USER: str = "Isiah Jordan"

# Get data from .env file as dictionary
CONFIG: dict = dotenv_values(".env")
EMAIL: str = CONFIG["GMAIL"]
PASSWORD: str = CONFIG["GMAIL_PASSWORD"]
SITE: str = CONFIG["STAGING_URL"]
WORKSPACE: str = CONFIG["STAGING_NAME"]
BROWSER: str = "firefox"
