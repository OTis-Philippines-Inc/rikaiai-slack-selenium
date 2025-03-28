from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from seleniumbase import BaseCase
import os, sys

# Add python files within project directory for import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config")))

class Message:
    def message_to_channel(self, sb: BaseCase, msg: str, channel: str) -> None:
        """
            Messaging through chosen channel.
            ----

            sb: test case associated with the BaseCase class.
            msg: text that will be sent to channel.
            channel: name of channel in slack.
        """
        
        # Traverse to channel
        self._traverse_to_channel(sb, channel)

        # Enter message
        sb.send_keys("div[role='textbox']", msg)
        sb.send_keys("div[role='textbox']", Keys.ENTER)

    def _traverse_to_channel(self, sb: BaseCase, channel: str) -> None:
        """
            Change channel in workspace.
            ----

            sb: test case associated with the BaseCase class.
            channel: name of channel in slack.
        """

        # Traverse to channel
        sb.click("#home")
        #sb.assert_element("xpath", "//span[text()='{channel}']", timeout=7)
        sb.click(f"span[data-qa='channel_sidebar_name_{channel}']")
        sb.assert_element("div[role='textbox']")

    def _find_message(self, sb: BaseCase, username: str, index: int) -> object:
        """
            Search message and scroll up to be detectable then pause the process.
            
            ----
            
            sb: test case associated with the BaseCase class.
            username: the account username sender.
            index: which chat using 0-based index will be selected and replaced.
        """
        messages: object = sb.find_elements(".offscreen")
        
        # This is to mimic user interaction authenticity
        action: object = ActionChains(sb.driver)
        index_track: int = 0

        # Search in thread for the name and message sent based on index count
        for msg in messages:
            if msg.text and msg.text == username and index_track == index:
                sb.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", msg)
                sb.sleep(5)
                # Edit message
                action.move_to_element(msg).perform()
                print(msg.text)
                return

            if msg.text == username:
                index_track+=1

        print("User Message: Not Found")

    def update_message(self, sb: BaseCase, sub: str, username: str, index: int, channel: str) -> None:
        """
            Update the message chosen by channel, name, and index count.
            ----
            
            sb: test case associated with the BaseCase class.
            sub: text that will replace the message.
            username: the account username sender.
            index: which chat using 0-based index will be selected and replaced.
            channel: name of channel in slack.
        """
        # Traverse to channel
        self._traverse_to_channel(sb, channel)
        sb.sleep(1)

        # Search in thread for the name and message sent based on index count
        self._find_message(sb, username, index)
        sb.click("button[data-qa='more_message_actions']", timeout=10)
        sb.click("button[data-qa='edit_message']", timeout=10)
        
        sb.send_keys("div[aria-label='Edit message']", Keys.CONTROL + "a")
        sb.send_keys("div[aria-label='Edit message']", Keys.BACKSPACE)
        sb.send_keys("div[aria-label='Edit message']", sub)
        sb.sleep(1)
        sb.send_keys("div[aria-label='Edit message']", Keys.ENTER)

    def delete_message(self, sb: BaseCase, username: str, index: int, channel: str) -> None:
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
        self._traverse_to_channel(sb, channel)
        sb.sleep(5)

        self._find_message(sb, username, index)
        sb.click("button[data-qa='more_message_actions']", timeout=10)
        sb.click("button[data-qa='delete_message']", timeout=10)
        sb.click("button[aria-label='Delete']", timeout=10)

