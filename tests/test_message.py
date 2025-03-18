from seleniumbase import BaseCase
import os, sys

# Add python files within project directory for import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "actions", "messagePage")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "actions", "loginPage")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config")))
from settings import USER, SITE
from login import Login
from message import Message

BaseCase.main(__name__, __file__)

class MessagePage(BaseCase):
    def test_message_update(self) -> None:
        Login().login_to_page(self)
        self.wait(5)
        Message().update_message(self, "Trest", "Isiah Jordan", 0,  "juan-autoamted-testing", "channel_sidebar_name_juan-autoamted-testing")
        self.wait(5)

        #import pdb; pdb.set_trace()

