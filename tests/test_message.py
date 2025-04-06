from seleniumbase import BaseCase
import os, sys

# Add python files within project directory for import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "actions", "messagePage")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "actions", "loginPage")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utilities")))
from settings import USER, EMAIL, SITE, CHANNEL, MSG_INPUT
from login import Login
from message import Message
from billing import Billing
from playback import Playback

BaseCase.main(__name__, __file__)

class MessagePage(BaseCase):
    def setUp(self):
        super().setUp()
        self.record = Playback(self.driver)

    def test_message_delete(self) -> None:
        self.record.start_recording("test_message_delete")
        Login().login_to_page(self, EMAIL, SITE)
        self.wait(5)
        
        # Delete Message
        msg_handle: object = Message(self)
        bill_handle: object = Billing(self, msg_handle)
        for channel in CHANNEL:
            # Fetch current bill score for channel
            bill_handle.update_bill() # Update current bll score
            points: float = bill_handle.get_channel_bill(channel) # Monitor difference in score
            for index, text, translation in MSG_INPUT:
                msg_handle.delete_message(USER, index, channel)
            
            bill_handle.update_bill()
            self.assert_equal(points, bill_handle.get_channel_bill(channel))

        # Closing the recording
        self.record.stop_and_save_recording()
        self.driver.close()



