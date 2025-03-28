import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seleniumbase import BaseCase
from actions.slackCommands.language_modal import LanguageModal
from actions.loginPage.login import Login
from utilities.playback import Playback


class LanguageModalTest(BaseCase):

    def setUp(self):
        super().setUp()
        self.record = Playback(self.driver)

    def test_language_modal(self):
        self.record.start_recording("test_language_modal")
        Login().direct_url(self)
        modal = LanguageModal()
        
        modal.select_channel(self)
        modal.enter_command(self, "/config-rikaiai language")
        self.wait(2)
        
        modal.select_target_scope(self)
        modal.select_source_language(self)
        modal.select_target_languages(self)
        self.click('button[data-qa="wizard_modal_next"]')
        self.wait(5)

        self.record.stop_and_save_recording()
        self.driver.close()
