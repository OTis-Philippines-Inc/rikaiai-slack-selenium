from seleniumbase import BaseCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os, sys

# Add python files within project directory for import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config")))

class Message:
    def message_to_channel(self, sb: BaseCase, msg: str, channel: str, attr_name: str) -> None:
        """
            Messaging through chosen channel.
            ----

            sb: test case associated with the BaseCase class.
            msg: text that will be sent to channel.
            channel: name of channel in slack.
            attr_name: data-qa convention placed in span of the slack nav bar attributed to channel.
        """
        
        # Traverse to channel
        self._traverse_to_channel(sb, channel, attr_name)

        # Enter message
        sb.send_keys("div[role='textbox']", msg)
        sb.send_keys("div[role='textbox']", Keys.ENTER)

    def _traverse_to_channel(self, sb: BaseCase, channel: str, attr_name: str) -> None:
        """
            Change channel in workspace.
            ----

            sb: test case associated with the BaseCase class.
            channel: name of channel in slack.
            attr_name: data-qa convention placed in span of the slack nav bar attributed to channel.
        """

        # Traverse to channel
        sb.click("#home")
        #sb.assert_element("xpath", "//span[text()='{channel}']", timeout=7)
        sb.click(f"span[data-qa='{attr_name}']")
        sb.assert_element("div[role='textbox']")
        

    def update_message(self, sb: BaseCase, sub: str, username: str, index: int, channel: str, attr_name: str) -> None:
        """
            Update the message chosen by channel, name, and index count.
            ----
            
            sb: test case associated with the BaseCase class.
            sub: text that will replace the message.
            username: the account username sender.
            index: which chat using 0-based index.
            channel: name of channel in slack.
            attr_name: data-qa convention placed in span of the slack nav bar attributed to channel.
        """
        # Traverse to channel
        self._traverse_to_channel(sb, channel, attr_name)
        sb.sleep(5)
        messages: object = sb.find_elements(".offscreen")
        
        # This is to mimic user interaction authenticity
        action: object = ActionChains(sb.driver)

        # Search in thread for the name and message sent based on index count
        for msg in messages:
            if msg.text and msg.text == username:
                if index == 0:
                    # Edit message
                    action.move_to_element(msg).perform()
                    sb.click("button[data-qa='more_message_actions']", timeout=10)
                    sb.click("button[data-qa='edit_message']", timeout=10)
                    
                    sb.send_keys("div[aria-label='Edit message']", "CTRL+A")
                    sb.send_keys("div[aria-label='Edit message']", "BACKSPACE")
                    sb.send_keys("div[aria-label='Edit message']", sub)
                    sb.send_keys("div[aria-label='Edit message']", "ENTER")
                    break
                index -= 1

    def delete_message(self, sb: BaseCase, username: str, index: int, channel: str, attr_name: str) -> None:
        """
            Delete the message chosen by channel, name, and index count.
            ----
            
            sb: test case associated with the BaseCase class.
            username: the account username sender.
            index: which chat using 0-based index.
            channel: name of channel in slack.
            attr_name: data-qa convention placed in span of the slack nav bar attributed to channel.
        """
        # Traverse to channel
        self._traverse_to_channel(sb, channel, attr_name)
        sb.sleep(5)
        messages: object = sb.find_elements(".offscreen")
        
        # This is to mimic user interaction authenticity
        action: object = ActionChains(sb.driver)

        # Search in thread for the name and message sent based on index count
        for msg in messages:
            if msg.text and msg.text == username:
                if index == 0:
                    # Edit message
                    action.move_to_element(msg).perform()
                    sb.click("button[data-qa='more_message_actions']", timeout=10)
                    sb.click("button[data-qa='delete_message']", timeout=10)
                    break
                index -= 1

