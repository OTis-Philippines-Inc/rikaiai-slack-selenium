import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))


import time
from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class Test:
    def direct_url(self, sb):
        # Get message and source_language
        message = "Testing"
        source_language = "en"

        body = sb.driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.PAGE_DOWN)  # Scroll down one page
        time.sleep(2)

        # Wait until the input field is available
        sb.wait_for_element("div[contenteditable='true']", timeout=10)

        # Find the Slack message input field
        input_field = sb.find_element("div[contenteditable='true']")

        # Click the input field to activate it
        input_field.click()
        time.sleep(1)  # Small delay to ensure it's active

        # Use JavaScript to insert text into Quill editor
        sb.execute_script("arguments[0].innerHTML = arguments[1];", input_field, message)

        # Press ENTER to send the message
        input_field.send_keys(Keys.ENTER)

        # Verify message is sent
        sb.wait_for_element(f'div[data-qa="message_content"]:contains("{message}")', timeout=10)
        sb.assert_element(f'div[data-qa="message_content"]:contains("{message}")')

        time.sleep(5)  # Small delay to ensure it's active
        

        # Wait for all reply bars to be present
        reply_bars = WebDriverWait(sb.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-qa='reply_bar']"))
        )

        # Click the last reply bar (most recent)
        if reply_bars:
            latest_reply_bar = reply_bars[-1]  # Get the last element
            sb.driver.execute_script("arguments[0].scrollIntoView();", latest_reply_bar)  # Scroll into view
            time.sleep(1)  # Small delay to ensure visibility
            latest_reply_bar.click()  # Click the latest reply bar
        else:
            raise Exception("No reply bars found on the page.")

        time.sleep(5)  # Small delay to ensure it's active

        sb.type("input[name='change_source_language']", source_language)
        input_field = sb.find_element("input[name='change_source_language']")
        input_field.send_keys(Keys.ENTER)
        time.sleep(10)  # Small delay to ensure it's active