from seleniumbase import BaseCase
from actions.loginPage.login import Login


class LoginPage(BaseCase):

    def test_direct_url(self):
        Login().direct_url(self)

