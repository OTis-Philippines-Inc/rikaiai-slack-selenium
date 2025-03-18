from seleniumbase import BaseCase
import os, sys

# Add python files within project directory for import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config")))

from settings import USER, SITE
from otp import fetch_slack_otp

class Login:
    def login_to_page(self, sb: BaseCase) -> None:
        """
            Automates login and otp process using Google API.

            ----
            sb: test case associated with the BaseCase class.
        """
        # Open Slack login page
        sb.get(SITE)

        # Enter login credentials
        sb.type('input[name="email"]', USER)
        sb.click('button[type="submit"]')

        # Fetch OTP code from email
        otp_code: str = fetch_slack_otp().replace("-", "")
        for i, digit in enumerate(otp_code, start=1):
            selector = f"[aria-label='digit {i} of 6']" 
            sb.click(selector)
            sb.send_keys(selector, digit)
            sb.wait(1)

        sb.wait(3)

        # Clicked on workspace
        sb.execute_script("document.querySelector('a').removeAttribute('target')")
        element: object = sb.find_element('a[aria-label="Open RikaiAI (Staging - Numbers00)"')
        workspace: str = element.get_attribute("href")

        # Open workspace
        sb.get(workspace)
        element = sb.find_element("xpath", "//a[contains(text(), 'use Slack in your browser')]")
        workspace = element.get_attribute("href")
        sb.get(workspace)

        sb.sleep(5)

