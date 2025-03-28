import os
import dotenv

dotenv.load_dotenv()
current_dir = os.path.dirname(os.path.abspath(__file__))


class Settings:
    def __init__(self):
        self.staging_url = os.getenv("STAGING_URL")
        self.gmail = os.getenv("GMAIL")
        self.staging_name = os.getenv("STAGING_NAME")


settings = Settings()
