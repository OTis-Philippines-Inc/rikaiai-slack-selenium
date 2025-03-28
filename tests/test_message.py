from seleniumbase import BaseCase
import os, sys

# Add python files within project directory for import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "actions", "messagePage")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "actions", "loginPage")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config")))
from settings import USER, EMAIL, SITE, CHANNEL
from login import Login
from message import Message

BaseCase.main(__name__, __file__)

class MessagePage(BaseCase):
    def test_message_delete(self) -> None:
        Login().login_to_page(self, EMAIL, SITE)
        self.wait(5)
        
        # Delete Message
        index: int = 0
        for channel in CHANNEL:
            for message_index in [0, 2]:
                # Index is to make sure that after deletion the message_index
                # will consider the changes on the list of user message
                Message().delete_message(self, USER, message_index-index, channel)
                index+=1

        #import pdb; pdb.set_trace()

