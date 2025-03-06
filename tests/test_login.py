from seleniumbase import BaseCase
from actions.loginPage.login import Login
from utilities.playback import Playback


class LoginPage(BaseCase):

    def setUp(self):
        super().setUp()
        self.record = Playback(self.driver)

    def test_direct_url(self):

        self.record.start_recording("test_direct_url")
        Login().direct_url(self)

        self.record.stop_and_save_recording()
        self.driver.close()
