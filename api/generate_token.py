from mail import OauthHandle, AccountHandle
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "config"))
from settings import TOKEN_NAME, SECRET_NAME, DIR_PATH, GMAIL_SCOPES

if __name__ == "__main__":
    # This is to make sure that we have the token.json
    # for authentication ready and validated to access
    # email automation
    OauthHandle.verify_token(
            DIR_PATH + "/" + TOKEN_NAME, 
            DIR_PATH + "/" + SECRET_NAME, 
            GMAIL_SCOPES)

    # TESTING REGION OF CODE
    # uncomment if needed
    
    # acc = AccountHandle(DIR_PATH + "/" + TOKEN_NAME,  GMAIL_SCOPES)
    # search = "Slack confirmation code: "
    # result = acc.search_email(search)["subject"][len(search):]
    # print(result)
