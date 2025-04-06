from google.oauth2.credentials import Credentials
import base64
from bs4 import BeautifulSoup
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "config"))

from googleapiclient.discovery import build
from settings import STRIP_OPT, SORT_OPT, MIN_DATE, TRIM_CONTENT, DATE_FORMAT
from datetime import datetime

class AccountHandle:
    def __init__(self, token_name: str, scopes: list):
        if not os.path.exists(token_name):
            raise ValueError("Token was not valid!! (HINT: invoke verify_token()")
        self.service: object = build("gmail", "v1", credentials=OauthHandle.get_token(token_name, scopes))

    def search_email(self, pattern: str, strip: STRIP_OPT = "left", by_date: SORT_OPT = "desc", limit: int=10) -> dict:
        """
            Search emails from service that mathces the pattern string and store it as a dictionary.
            ----
            
            pattern: string that will matched to subject.
            strip: STRIP_OPT provides full, left, or right options method of comparing string.
            by_date: sort by None, Asc, or Desc.
            limit: how many messages would be compared before stopage.
        """
        
        # Fetch threads that matches the subject
        query: str = None
        
        match strip:
            case "full": # Complete match
                query = f'subject:"{pattern}"'
            case "right": # Prefix
                query = f'subject:"{pattern}*"'
            case "left": # Suffix
                query = f'subject:"*{pattern}"'
            case _:
                raise ValueError("Strip option is not valid!!!")

        message: list = self.service.users().messages().list(userId="me", q=query, maxResults=limit).execute().get("messages", [])
        if not message:
            print("No thread waws found that matches the query...")
            return None
        
        # Fetch the details that best match the request
        mail: dict = None
        for msg in message:
            _mail: dict = self.format_detail(msg)

            if not mail or mail["date"] < _mail["date"]:
                mail = _mail

        return mail


    def format_detail(self, msg: dict) -> dict:
        """
            Taking a message thread, decoupling into 4 sections: header, subject, content, date.
            ----

            msg: an element of the get list meessages Google API.
        """
        data: object = self.service.users().messages().get(userId="me", id=msg["id"], format="full").execute()

        # Individual parts of the message
        headers: str = data["payload"]["headers"]
        sender: str = next((h["value"] for h in headers if h["name"] == "From"), "Unknown Sender")
        subject: str = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        date: str = next((h["value"] for h in headers if h["name"] == "Date"), "No Date")
        content: str = self.extract_body(data["payload"])
        strdate: str = date # Just a copy for the string equivalent

        if not date == "No Date":
            date = datetime.strptime(date, DATE_FORMAT)
        else:
            date = MIN_DATE

        return {
                    "date": date,
                    "strdate": strdate,
                    "sender": sender,
                    "subject": subject,
                    "content": content[:TRIM_CONTENT]
                }


    def extract_body(self, payload: str) -> str:
        """
            Extract plain text from an email payload.
            ----

            payload: contents of the email (header, body, ...).
        """
        if "data" in payload["body"]:  # Direct body
            return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="ignore")

        if "parts" in payload:  # Multipart email (HTML + Plain text)
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain":  # Extract plain text
                    return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="ignore")
                if part["mimeType"] == "text/html":  # Extract HTML (fallback)
                    html_content = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="ignore")
                    return BeautifulSoup(html_content, "html.parser").get_text()

        return "No Content"
    

class OauthHandle:
    @staticmethod
    def verify_token(token_name: str, secret_name: str, scopes: list) -> None:
        """
            Generates and monitors token.json from the client_secret.json from the token_name
            and secret_name.
            ----

            token_name: relative path of token.json location and naming convo.
            secret_name: relative path of secret.json location and naming convo.
            scopes: modes provided by the Google API.

        """

        # Load token from the token name
        creds: object = OauthHandle.get_token(token_name, scopes)

        # Verify status for client token
        if not creds or not creds.valid:
            # Refresh token
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            # Open gmail account verification
            else:
                flow: object = InstalledAppFlow.from_client_secrets_file(secret_name, scopes)
                creds = flow.run_local_server(port=0)

            # Generate or overriding token.json
            with open(token_name, "w") as token:
                token.write(creds.to_json())
    
    @staticmethod
    def get_token(token_name, scopes) -> object:
        """
            Load token.json.
            ----

            token_name: relative path of token.json location and naming convo.
            scopes: modes provided by the Google API.
        """

        if os.path.exists(token_name):
            return Credentials.from_authorized_user_file(token_name, scopes)
        
        return None


