from seleniumbase import BaseCase
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "actions", "messagePage")))
from selenium.webdriver.common.keys import Keys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config")))
from message import Message

class SlackConfig:
    def __init__(self, sb: BaseCase, sender: Message):
        self.sb = sb
        self.sender = sender
        self.source: str = "English" # langauge source
        self.target: list = [] 
    
    def set_source(self, language: str) -> None:
        self.source = language

    def set_target(self, languages: list) -> None:
        self.target = languages

    def set_language(self, channel: str, is_translate: bool) -> None:
        self.sender.message_to_channel("/config-rikaiai langauge", channel)
        self.sb.assert_element("input[role='combobox']")
        dropdown: list = self.sb.find_elements("input[role='combobox']")

        # Set source
        dropdown[1].send_keys(self.source)
        dropdown[1].send_keys(Keys.ENTER)

        # Set target language
        for target in self.target:
            self.sb.send_keys("div[role='combobox']", target)
            self.sb.send_keys("div[role='combobox']", Keys.ENTER)

        if not is_translate:
            # Set to do not translate
            self.click("input[role='checkbox']", timeout=10)

        self.sb.click("button[data-qa='wizard_modal_next']", timeout=10)

