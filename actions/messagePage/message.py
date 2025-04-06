from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from seleniumbase import BaseCase
from dataclasses import dataclass
from typing import List, Optional

import os, sys

# Add python files within project directory for import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config")))


@dataclass
class Reply:
    """
        Data class representing a reply message.
        ----
        sender: Name of the sender.
        message: The message text.
        (Add more fields as necessary)
    """
    sender: str
    message: str


class Message:
    def __init__(self, sb: BaseCase) -> None:
        """
            Initialize the Message object.
            ----
            sb: test case associated with the BaseCase class.
        """
        self.sb = sb

    def message_to_channel(self, msg: str, channel: str) -> None:
        """
            Messaging through chosen channel.
            ----
            sb: test case associated with the BaseCase class.
            msg: text that will be sent to channel.
            channel: name of channel in slack.
        """
        self._traverse_to_channel(channel)
        self.input_textbox(msg)

    def input_textbox(self, msg: str) -> None:
        """
            Type sequence of string to textbox.
            ----
            sb: test case associated with the BaseCase class.
            msg: text that will be sent to channel.
        """
        self.sb.send_keys("div[role='textbox']", msg)
        self.sb.send_keys("div[role='textbox']", Keys.ENTER)

    def _traverse_to_channel(self, channel: str) -> None:
        """
            Change channel in workspace.
            ----
            sb: test case associated with the BaseCase class.
            channel: name of channel in slack.
        """
        self.sb.click("#home")
        self.sb.click(f"span[data-qa='channel_sidebar_name_{channel}']")
        self.sb.assert_element("div[role='textbox']")

    def get_reply(self, username: str, replier: str, index: int, channel: str) -> List[str]:
        """
            Get the reply based on the index count of the message.
            ----
            sb: test case associated with the BaseCase class.
            username: the account username message sender.
            replier: the account username that replies to the sender.
            index: relative to chat using 0-based index will be selected.
            channel: name of channel in slack.
        """
        # Traverse to channel
        self._traverse_to_channel(channel)
        self.sb.refresh_page()
        self.sb.wait(5)

        # Find the message index based on username and index count
        message_index = self._find_message(username, index, self._scroll_to_message)
        self.sb.wait_for_attribute(".c-message__reply_count", "data-qa", timeout=10)
        
        # Get reply index from message content blocks
        reply_index = self._get_reply_index(message_index)
        print(f"Using reply index {reply_index} (original message index: {message_index})")
        
        self.sb.find_elements(".c-message__reply_count")[reply_index].click()
        self.sb.wait(5)

        # Get replies by using the innerHTML
        replies_html = self.sb.find_element("div[data-qa='flexpane_body']").get_attribute("innerHTML")
        self.sb.wait(4)
        return self._parse_replies(replies_html, replier)

    def _get_reply_index(self, message_index: int) -> int:
        """
            Determine the reply index by inspecting message content blocks.
            ----
            message_index: the index of the message as found by _find_message.
        """
        blocks = self.sb.find_elements("div[data-qa='message_content']")
        index_match: int = 0
        for index_track, block in enumerate(blocks):
            soup = BeautifulSoup(block.get_attribute("innerHTML"), "html.parser")
            if soup.find("button", attrs={"data-qa": "reply_bar_count"}):
                if index_track == message_index:
                    break
                index_match += 1
        return index_match

    def _parse_replies(self, html: str, username: str) -> List[str]:
        """
            Parse the reply pane HTML and extract reply messages.
            ----
            html: innerHTML content of the reply pane.
            username: the account username that replied to the message.
        """
        soup = BeautifulSoup(html, "html.parser")
        reply_elements = soup.find_all("div", attrs={"aria-roledescription": "message"})
        messages_reply: List[str] = []
        for rep in reply_elements:
            name_tag = rep.find("button", attrs={"data-qa": "message_sender_name"})
            if name_tag:
                name = name_tag.get_text(strip=True)
                if name == username:
                    message_contents = rep.find_all('div', attrs={'data-qa': 'bk_section_block'})
                    messages = [msg.get_text(strip=True) for msg in message_contents]
                    messages_reply.extend(messages)
        return messages_reply

    def _scroll_to_message(self, status: int, index: int, *args) -> Optional[int]:
        """
            Scroll the given message element into view and perform actions.
            ----
            status: if the callback was called because of a match, increment, or non-matching. (0, 1, 2)
            index: relative index value.
            args: expects the message element and optionally an updated index.
        """
        if status == 0 and args:
            message_element = args[0]
            self.sb.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", message_element)
            self.sb.wait(2)
            ActionChains(self.sb.driver).move_to_element(message_element).perform()
            if len(args) > 1:
                return args[1]
        return None

    def _find_message(self, username: str, index: int, callback: object) -> int:
        """
            Search message and become detectable then pause the process.
            Also returns the index if required.
            ----
            sb: test case associated with the BaseCase class.
            username: the account username sender.
            index: which chat using 0-based index will be selected.
            callback: function or method that will be called after matches.
        """
        messages = self.sb.find_elements("span[data-qa='message_sender']")
        index_match: int = 0

        for index_track, msg in enumerate(messages):
            sender: str = msg.text.split("\n")[0]
            print(f"Found sender: {sender} at index {index_match}")  # Debug line
            if sender == username:
                print(f"Found Username Match: {sender}, {index_match}")
                if index_match == int(index):
                    print("Successful Search")
                    callback(0, index_match, msg, index_track)
                    return index_track
                else:
                    print(f"Index: {index} does not match with Proceeding Index: {index_match}")
                    callback(1, index_match, msg)
                    index_match += 1
            else:
                callback(2, index_match, msg)

        self.sb.fail(f"Message from '{username}' at index {index} not found.")
        return -1
    
    def config_language(self, channel: str) -> None:
        """"
            Set configuration for language by channel.
            ----
            channel: name of channel in slack"""

        self.message_to_channel("/config-rikaiai language")

    def update_message(self, sub: str, username: str, index: int, channel: str) -> None:
        """
            Update the message chosen by channel, name, and index count.
            ----
            sb: test case associated with the BaseCase class.
            sub: text that will replace the message.
            username: the account username sender.
            index: which chat using 0-based index will be selected and replaced.
            channel: name of channel in slack.
        """
        self._traverse_to_channel(channel)
        self.sb.refresh_page()
        self.sb.wait(5)

        self._find_message(username, index, self._scroll_to_message)
        self.sb.wait_for_element("button[data-qa='more_message_actions']", timeout=10)
        self.sb.click("button[data-qa='more_message_actions']", timeout=10)
        self.sb.click("button[data-qa='edit_message']", timeout=10)
        
        self.sb.send_keys("div[aria-label='Edit message']", Keys.CONTROL + "a")
        self.sb.send_keys("div[aria-label='Edit message']", Keys.BACKSPACE)
        self.sb.send_keys("div[aria-label='Edit message']", sub)
        self.sb.sleep(1)
        self.sb.send_keys("div[aria-label='Edit message']", Keys.ENTER)

    def delete_message(self, username: str, index: int, channel: str) -> None:
        """
            Delete the message chosen by channel, name, and index count.
            ----
            sb: test case associated with the BaseCase class.
            username: the account username sender.
            index: which chat using 0-based index.
            channel: name of channel in slack.
        """
        self._traverse_to_channel(channel)
        self.sb.scroll_to_bottom()

        self._find_message(username, index, self._scroll_to_message)
        self.sb.sleep(5)
        self.sb.click("button[data-qa='more_message_actions']", timeout=10)
        self.sb.click("button[data-qa='delete_message']", timeout=10)
        self.sb.click("button[aria-label='Delete']", timeout=10)

