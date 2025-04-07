import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seleniumbase import BaseCase
from actions.slackCommands.language_modal import LanguageModal
from actions.loginPage.login import Login
from utilities.playback import Playback
from selenium.webdriver.common.by import By


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

        modal.enter_command(self, "안녕하세요")
        self.wait(2)

        reply_bars = self.find_elements('div[data-qa="reply_bar"]')        
        most_recent_reply = reply_bars[-1]
        most_recent_reply.click()
        self.wait(2)

        self.wait_for_element_present('div[data-qa="message_content"]')
        message_blocks = self.find_elements('div[data-qa="message_content"]')    
        most_recent_message = message_blocks[-1]
        
        try:
            most_recent_message.find_element(By.CSS_SELECTOR, 'img[alt=":cn:"]')
            is_chinese = True
        except:
            is_chinese = False
        
        assert is_chinese, "Translation is not in Chinese (no CN flag found)"
        
        self.record.stop_and_save_recording()
        self.driver.close()