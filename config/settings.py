import os
import dotenv

dotenv.load_dotenv()
current_dir = os.path.dirname(os.path.abspath(__file__))


class Settings:
    def __init__(self):
        self.staging_url = os.getenv("STAGING_URL")
        self.gmail = os.getenv("GMAIL")
        self.password = os.getenv("PASSWORD")
        self.staging_name = os.getenv("STAGING_NAME")
        self.channel_name = os.getenv("CHANNEL_NAME")
        self.source_language = os.getenv("SOURCE_LANGUAGE")
        self.target_languages = os.getenv("TARGET_LANGUAGES")

settings = Settings()
