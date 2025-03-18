import sys, os, time

sys.path.append(os.path.abspath(os.getcwd() + "/api"))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config")))

from mail import AccountHandle
from settings import TOKEN_NAME, GMAIL_SCOPES, DIR_PATH

def fetch_slack_otp() -> str:
    """
        Fetch OTP code from Google API
    """
    search: str = "Slack confirmation code: "
    time.sleep(5)
    return AccountHandle(DIR_PATH + "/" + TOKEN_NAME, GMAIL_SCOPES).search_email(search)["subject"][len(search):]

