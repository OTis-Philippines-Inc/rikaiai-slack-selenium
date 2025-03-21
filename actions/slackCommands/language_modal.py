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

    '''
    def select_target_scope(self, sb, target_scope):
        Target Scope
        <div class="p-block_kit_input_block__element c-search-select" data-qa="language_settings_modal_change_target_scope"><div role="presentation" class="c-select_input__wrapper c-select_input--medium c-select_input--with_icon_right" data-qa="language_settings_modal_change_target_scope-wrapper" style="width: 100%;"><div class="c-select_input__input_container"><input spellcheck="false" aria-autocomplete="list" aria-expanded="true" aria-owns="language_settings_modal_change_target_scope-language_settings_modal_target_scope_input-2daceb40_38fd_49b4_9539_231de7efe86e_listbox" aria-required="true" aria-label="Whether to apply settings to the workspace or this channel only" aria-labelledby="language_settings_modal_change_target_scope-language_settings_modal_target_scope_input-2daceb40_38fd_49b4_9539_231de7efe86e-label" aria-describedby="language_settings_modal_change_target_scope-language_settings_modal_target_scope_input-2daceb40_38fd_49b4_9539_231de7efe86e_initial-focus" data-qa="language_settings_modal_change_target_scope-input" role="combobox" aria-invalid="false" autocomplete="off" class="c-input_text c-select_input" id="language_settings_modal_change_target_scope-language_settings_modal_target_scope_input-2daceb40_38fd_49b4_9539_231de7efe86e" name="language_settings_modal_change_target_scope-language_settings_modal_target_scope_input-2daceb40_38fd_49b4_9539_231de7efe86e" type="text" value="" placeholder="Whether to apply settings to the workspace or this channel only"></div><div class="c-select_input__icon_container"><span class="c-select_input__icon"><svg data-xh2="true" data-qa="caret-down" aria-hidden="true" viewBox="0 0 20 20" class="" style="--s: 20px;"><path fill="currentColor" fill-rule="evenodd" d="M5.72 7.47a.75.75 0 0 1 1.06 0L10 10.69l3.22-3.22a.75.75 0 1 1 1.06 1.06l-3.75 3.75a.75.75 0 0 1-1.06 0L5.72 8.53a.75.75 0 0 1 0-1.06" clip-rule="evenodd"></path></svg></span></div></div></div>

        Workspace
        <div aria-selected="true" class="c-select_options_list__option c-select_options_list__option--selected" data-qa="language_settings_modal_change_target_scope_option_0" id="language_settings_modal_change_target_scope-language_settings_modal_target_scope_input-580bafe3_6bf0_466f_8ef7_be72d21f8d16_option_0" role="option" tabindex="-1" aria-setsize="2" aria-posinset="1" style="height: 28px; left: 0px; position: absolute; top: 0px; width: 100%;"><span class="c-select_options_list__selected" aria-hidden="true"></span><span data-qa="workspace" class="c-select_options_list__option_label"><div class="p-block-kit-select_options"><div class="p-plain_text_element" data-qa="bk-plain_text_element"><span dir="auto">Workspace</span></div></div></span></div>

        Channel
        <div aria-selected="false" class="c-select_options_list__option" data-qa="language_settings_modal_change_target_scope_option_1" id="language_settings_modal_change_target_scope-language_settings_modal_target_scope_input-580bafe3_6bf0_466f_8ef7_be72d21f8d16_option_1" role="option" tabindex="-1" aria-setsize="2" aria-posinset="2" style="height: 28px; left: 0px; position: absolute; top: 28px; width: 100%;"><span data-qa="channel" class="c-select_options_list__option_label"><div class="p-block-kit-select_options"><div class="p-plain_text_element" data-qa="bk-plain_text_element"><span dir="auto">Channel</span></div></div></span></div>

    def select_source_language(self, sb, source_language[]):
        Source Language
        <input spellcheck="false" aria-autocomplete="list" aria-owns="language_settings_modal_change_source_language-language_settings_modal_source_language_input-580bafe3_6bf0_466f_8ef7_be72d21f8d16_listbox" aria-required="true" aria-label="First select the source language" aria-labelledby="" aria-describedby="language_settings_modal_change_source_language-language_settings_modal_source_language_input-580bafe3_6bf0_466f_8ef7_be72d21f8d16_initial-focus" data-qa="language_settings_modal_change_source_language-input" role="combobox" aria-invalid="false" autocomplete="off" class="c-input_text c-select_input" id="language_settings_modal_change_source_language-language_settings_modal_source_language_input-580bafe3_6bf0_466f_8ef7_be72d21f8d16" name="language_settings_modal_change_source_language-language_settings_modal_source_language_input-580bafe3_6bf0_466f_8ef7_be72d21f8d16" placeholder="First select the source language" type="text" value="" aria-expanded="false">

    def select_target_languages(self, sb, target_languages[]):
        Target Languages
        <input spellcheck="false" aria-autocomplete="list" aria-owns="language_settings_modal_change_source_language-language_settings_modal_source_language_input-580bafe3_6bf0_466f_8ef7_be72d21f8d16_listbox" aria-required="true" aria-label="First select the source language" aria-labelledby="" aria-describedby="language_settings_modal_change_source_language-language_settings_modal_source_language_input-580bafe3_6bf0_466f_8ef7_be72d21f8d16_initial-focus" data-qa="language_settings_modal_change_source_language-input" role="combobox" aria-invalid="false" autocomplete="off" class="c-input_text c-select_input" id="language_settings_modal_change_source_language-language_settings_modal_source_language_input-580bafe3_6bf0_466f_8ef7_be72d21f8d16" name="language_settings_modal_change_source_language-language_settings_modal_source_language_input-580bafe3_6bf0_466f_8ef7_be72d21f8d16" placeholder="First select the source language" type="text" value="" aria-expanded="false">
    '''