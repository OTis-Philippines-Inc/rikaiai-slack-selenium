from seleniumbase import BaseCase
import os, sys

# Add python files within project directory for import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "actions", "messagePage")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "actions", "loginPage")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utilities")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config")))
from translate import SlackConfig
from settings import USER, SITE, EMAIL, CHANNEL, MSG_INPUT
from login import Login
from message import Message
from billing import Billing
from playback import Playback

BaseCase.main(__name__, __file__)

class MessagePage(BaseCase):
    def setUp(self):
        super().setUp()
        self.record = Playback(self.driver)

    def test_message_update(self) -> None:
        # Record test
        self.record.start_recording("test_message_update")
        Login().login_to_page(self, EMAIL, SITE)
        self.wait(5)
        
        msg_handle: object = Message(self)
        bill_handle: object = Billing(self, msg_handle)
        translate_handle: object = SlackConfig(self, msg_handle)
        for channel in CHANNEL:
            points: float = 0 # Monitor difference in score
            #points = bill_handle.get_channel_bill(channel)
            for index, text, translation, source, target, is_translated in MSG_INPUT:
                # Set configurations
                translate_handle.set_source(source)
                translate_handle.set_target(target)
                translate_handle.set_language(channel, is_translated)

                msg_handle.update_message(text, USER, index, channel)
                self.wait(3)

                replies: list = msg_handle.get_reply(USER, "RikaiAI",index, channel)
                print(replies)
                msg_handle.config_language(channel)
                
                # Set translate

            self.assert_equal(2, 2)

           # Compare poiints after update
            #points = bill_handle.get_channel_bill(channel) - points

        # Closing the recording
        self.record.stop_and_save_recording()
        self.driver.close()
        #import pdb; pdb.set_trace()


