import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

# Get the absolute path of the folder containing api_utils.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../api")))

import time
from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from api_utils import send_verification_email, get_verification_code
from config.settings import settings as cfg


class Login:
    def direct_url(self, sb):
        sb.maximize_window()
        sb.open(cfg.staging_url)
        sb.wait_for_ready_state_complete()

        sb.type("input[data-qa='signin_domain_input']", cfg.staging_name)
        sb.click("button[data-qa='submit_team_domain_button']")
        sb.wait_for_ready_state_complete()

        sb.type("input[data-qa='email_field']", cfg.gmail)
        sb.click("button[data-qa='submit_button']")
        sb.wait_for_ready_state_complete()

        # verification_code = "123456"  # Replace this with the actual code

        # Fetch verification code
        verification_code = get_verification_code()
        if not verification_code:
            sb.fail("Verification code not found!")


        # Loop through each digit and type it into the corresponding field
        for i, digit in enumerate(verification_code, start=1):
            input_field = sb.find_element(f'input[aria-label="digit {i} of 6"]')
            input_field.send_keys(digit)  # Simulates real keystrokes
        sb.wait_for_ready_state_complete()  # Wait
