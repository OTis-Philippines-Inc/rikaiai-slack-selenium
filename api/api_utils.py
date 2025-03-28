import firebase_admin
import re
from firebase_admin import auth, credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from bs4 import BeautifulSoup

import os

# Get the absolute path to the JSON file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
json_path = os.path.join(BASE_DIR, "../.credentials/firebase_adminsdk.json")  # Adjust path

if not os.path.exists(json_path):
    raise FileNotFoundError(f"Firebase credentials file not found: {json_path}")

cred = credentials.Certificate(json_path)  # Load Firebase credentials

firebase_admin.initialize_app(cred)

def send_verification_email(user_email):
    """Trigger email verification via Firebase Authentication."""
    user = auth.get_user_by_email(user_email)
    auth.update_user(user.uid, email_verified=False)
    print(f"Verification email triggered for {user.email}")

# === GMAIL API SETUP (Google Cloud Managed) === #
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_gmail_service():
    """Authenticate using OAuth and return Gmail API service."""

    # Get absolute path to client_secret.json inside credentials/
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
    json_path = os.path.join(BASE_DIR, "../.credentials/client_secret.json")  # Adjust filename if needed

    # Verify if file exists before proceeding
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Client secret file not found: {json_path}")

    # Authenticate using OAuth
    flow = InstalledAppFlow.from_client_secrets_file(json_path, SCOPES)
    creds = flow.run_local_server(port=8080)  # Ensure it matches the URI set in Google Cloud

    return build("gmail", "v1", credentials=creds)

def extract_verification_code(msg):
    """Extracts the verification code from the email body."""
    if "parts" in msg["payload"]:  # Check if the email has multiple parts
        for part in msg["payload"]["parts"]:
            if part["mimeType"] == "text/plain":
                body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                soup = BeautifulSoup(body, "html.parser")
                text = soup.get_text().strip()
                print("Extracted text:", text)  # Debugging output
                return extract_code_from_text(text)
    elif "body" in msg["payload"]:  # Handle single-part emails
        body = base64.urlsafe_b64decode(msg["payload"]["body"]["data"]).decode("utf-8")
        soup = BeautifulSoup(body, "html.parser")
        text = soup.get_text().strip()
        print("Extracted text:", text)  # Debugging output
        return extract_code_from_text(text)
    return None

def extract_code_from_text(text):
    """Extracts a verification code in the format 'XXX-XXX' and removes the hyphen."""
    match = re.search(r"\b[A-Z0-9]{3}-[A-Z0-9]{3}\b", text)  # Match XXX-XXX format
    if match:
        return match.group(0).replace("-", "")  # Remove the hyphen before returning
    return None


def get_verification_code():
    """Fetches the latest unread email containing a verification code."""
    service = get_gmail_service()

    # Fetch only UNREAD emails with "Verify your email" in the subject
    results = service.users().messages().list(userId="me", q="is:unread subject:Slack confirmation code", maxResults=1).execute()
    messages = results.get("messages", [])

    if not messages:
        print("No unread verification email found.")
        return None

    # Get the most recent unread email
    msg = service.users().messages().get(userId="me", id=messages[0]["id"], format="full").execute()
    return extract_verification_code(msg)