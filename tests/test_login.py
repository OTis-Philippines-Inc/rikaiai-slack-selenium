from seleniumbase import BaseCase
import os, sys

# Add python files within project directory for import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "actions", "loginPage")))

from login import Login

BaseCase.main(__name__, __file__)

class LoginPage(BaseCase):
    def test_login(self) -> None:
        Login().login_to_page(self)
        self.wait(5)
        #import pdb; pdb.set_trace()
