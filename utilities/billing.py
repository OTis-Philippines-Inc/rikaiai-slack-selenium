import sys, os, re
from selenium.webdriver.common.keys import Keys
import logging
from seleniumbase import BaseCase

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "actions", "messagePage")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config")))
from message import Message

class Billing:
    def __init__(self, driver: BaseCase, sender: Message):
        """
            Manage the billing points per channel
        """
        self.driver = driver
        self.sender = sender
        self.bill: dict = None
       
    def view_bill(self) -> object:
        self.input_textbox("/billing-rikaiai")
        self.driver.send_keys("div[role='textbox']", Keys.ENTER)
           
        # Get parent and html of the tag
        self.driver.sleep(5)
        # Get html list of the channel points
        list_of_bill: object = self.driver.find_elements("[data-qa='message_content']")[-1].get_attribute("innerHTML")
        
        return list_of_bill

    def update_bill(self) -> None:
        """
            Update the list of channel points
        """

        list_of_bill: object = self.view_bill()
        # Breakdown the html into necessary channel points and name
        channel_bill_extract: list = re.findall(r"#[\x28-\x7a]+\s\d+\.\d+", list_of_bill) 

        # Convert channel bill into dictionary
        for channel in channel_bill_extract:
            channel_name, channel_score = channel.split(":")
            # Remove Unecessary characters like hashtag or stuck html tag
            channel_name = channel_name[1:].rstrip("</a>")
            self.bill[channel_name] = channel_score
            
    def get_channel_bill(self, channel: str) -> float:
        """
            View channel billing score from using the rikaiai API and then returns
            the score.
            ----

            channel: name of channel in slack.
        """
        
        return float(channel_bill[channel])
    
    def compute_score(self, msg: str, status: int) -> float:
        """
            Given a string, applying the rules of billing. Returns
            the computation of the msg bill.
            ----

            msg: message that will be used to compute.
            status: 0, 1, 2 (translation), 3 (update)
        """
        match status:
            case 0:
                return float(len(msg))
            case 1:
                return float(len(msg)) * 0.5
            case 2:
                return float(len(msg)) * 0.25
            case 3:
                return float(len(msg)) * 0.125
                

