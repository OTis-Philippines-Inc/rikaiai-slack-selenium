import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from seleniumbase import BaseCase
from config.settings import settings as cfg
from actions.loginPage.login import Login


class LanguageModal:
    def select_channel(self, sb):
        sb.click(f"span[data-qa='channel_sidebar_name_{cfg.channel_name}']")

    def enter_command(self, sb, command):
        sb.type("div.ql-editor[role='textbox']", command)
        sb.send_keys("div.ql-editor[role='textbox']", "\n")

    def select_target_scope(self, sb):
        sb.click("[data-qa='language_settings_modal_change_target_scope']")
        sb.click("[data-qa='language_settings_modal_change_target_scope_option_1']") # option_0 for Workspace, option_1 for Channel
        sb.wait(5)

    def select_source_language(self, sb):
        sb.type("[data-qa='language_settings_modal_change_source_language-input']", cfg.source_language)
        sb.wait_for_element_visible("[data-qa='language_settings_modal_change_source_language-options-list']", timeout=5)
        sb.click(f"//div[contains(@class, 'c-select_options_list__option')]//div[contains(@class, 'p-plain_text_element')]//span[text()='{cfg.source_language}']/ancestor::div[contains(@class, 'c-select_options_list__option')]")

    def select_target_languages(self, sb):
        sb.click("[data-qa='language_settings_modal_change_target_languages-input']")
        
        initial_input = cfg.target_languages[:3]
        sb.type("[data-qa='language_settings_modal_change_target_languages-input']", initial_input)
        
        sb.wait(1)

        if sb.is_element_visible("[data-qa='language_settings_modal_change_target_languages-options-list']"):
            option_xpath = (
                "//div[contains(@class, 'c-select_options_list__option')]"
                "//div[contains(@class, 'p-plain_text_element')]"
                f"//span[text()='{cfg.target_languages}']"
                "/ancestor::div[contains(@class, 'c-select_options_list__option')]"
            )
            sb.click(option_xpath)
            
        sb.wait(1)
        sb.assert_element_present(f"//span[contains(text(), '{cfg.target_languages}')]")