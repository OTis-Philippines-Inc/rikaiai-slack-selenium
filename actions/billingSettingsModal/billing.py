import os
import sys
from datetime import datetime
import re
import logging
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from seleniumbase import BaseCase
from config.settings import settings as cfg
from tests.test_data.billing_test_data import (
    VALID_CARD_DATA, VALID_ADDRESS_DATA, INVALID_CARD_DATA,
    INVALID_ADDRESS_DATA, PLAN_DATA, ERROR_MESSAGES, SUCCESS_MESSAGES
)

# Set up logging
logger = logging.getLogger(__name__)

class BillingSettingsModal:
    """A class to handle all billing settings modal interactions and validations.
    
    This class provides methods for interacting with the billing settings modal,
    including opening the modal, verifying billing information, updating payment
    details, and validating various billing-related data.
    """

    def __init__(self):
        """Initialize the BillingSettingsModal class."""
        self.valid_card_numbers = VALID_CARD_DATA
        self.valid_addresses = VALID_ADDRESS_DATA
        self.plan_data = PLAN_DATA
        self.error_messages = ERROR_MESSAGES
        self.success_messages = SUCCESS_MESSAGES

    def open_billing_settings(self, sb):
        """Open the billing settings modal and verify it's loaded correctly.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
            
        Raises:
            TimeoutError: If the billing settings page fails to load.
        """
        sb.maximize_window()
        sb.open(cfg.staging_url)
        sb.wait(5)

        # Login first
        sb.type("#signup_email", cfg.gmail)
        sb.wait(5)
        sb.click("#submit_btn")

        # Wait for login to complete
        for _ in range(60):
            if sb.is_text_visible(cfg.staging_name, ".p-ia4_home_header_menu__team_name"):
                break
            sb.wait(1)

        # Click on the menu button to open settings
        sb.click(".p-ia4_home_header_menu__button")
        sb.wait(2)

        # Click on billing settings in the menu
        sb.click("a[href='/admin/billing']")
        sb.wait(5)

        # Verify billing settings page is loaded
        sb.assert_element_visible(".p-billing_page", timeout=10)
        sb.wait(5)

    def verify_billing_plan(self, sb):
        """Verify the current billing plan details and validate the information.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
            
        Raises:
            AssertionError: If any billing plan details are missing or invalid.
        """
        # Verify plan type is visible
        sb.assert_element_visible(".p-billing_plan_type", timeout=10)
        
        # Verify plan details section
        sb.assert_element_visible(".p-billing_plan_details", timeout=10)
        
        # Verify billing amount
        amount_element = sb.get_element(".p-billing_amount")
        amount_text = amount_element.text
        self._validate_currency_format(amount_text)
        
        # Verify billing cycle
        sb.assert_element_visible(".p-billing_cycle", timeout=10)
        
        # Verify next billing date
        date_element = sb.get_element(".p-billing_next_date")
        date_text = date_element.text
        self._validate_date_format(date_text)
        
        sb.wait(2)

    def update_billing_info(self, sb):
        """Update billing information with validation.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
            
        Raises:
            ValueError: If the provided billing information is invalid.
        """
        # Click on edit billing info button
        sb.click(".p-billing_edit_button")
        sb.wait(2)

        # Update billing address with validation
        self._update_billing_address(sb)
        
        # Update payment method with validation
        self._update_payment_method(sb)
        
        # Save changes
        sb.click(".p-billing_save_button")
        sb.wait(5)
        
        # Verify success message
        sb.assert_element_visible(".p-billing_success_message", timeout=10)
        sb.wait(2)

    def verify_payment_history(self, sb):
        """Verify payment history section and validate payment records.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
            
        Raises:
            AssertionError: If payment history is invalid or incomplete.
        """
        # Click on payment history tab
        sb.click(".p-billing_payment_history_tab")
        sb.wait(2)
        
        # Verify payment history table is visible
        sb.assert_element_visible(".p-billing_payment_history_table", timeout=10)
        
        # Verify table headers
        self._verify_payment_history_headers(sb)
        
        # Verify and validate payment records
        self._validate_payment_records(sb)
        
        sb.wait(2)

    def _validate_currency_format(self, amount_text):
        """Validate that the amount follows proper currency format.
        
        Args:
            amount_text (str): The amount text to validate.
            
        Raises:
            ValueError: If the currency format is invalid.
        """
        currency_pattern = r'^\$?\d+(\.\d{2})?$'
        if not re.match(currency_pattern, amount_text):
            raise ValueError(f"Invalid currency format: {amount_text}")

    def _validate_date_format(self, date_text):
        """Validate that the date follows proper format.
        
        Args:
            date_text (str): The date text to validate.
            
        Raises:
            ValueError: If the date format is invalid.
        """
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid date format: {date_text}")

    def _update_billing_address(self, sb):
        """Update billing address with validation.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
        """
        address_fields = {
            '.p-billing_address_input': '123 Test Street',
            '.p-billing_city_input': 'Test City',
            '.p-billing_state_input': 'Test State',
            '.p-billing_zip_input': '12345',
            '.p-billing_country_input': 'Test Country'
        }
        
        for field, value in address_fields.items():
            sb.type(field, value)
            sb.wait(1)

    def _update_payment_method(self, sb):
        """Update payment method with validation.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
        """
        sb.click(".p-billing_payment_method_button")
        sb.wait(2)
        
        # Use a valid card number
        sb.type(".p-billing_card_number", self.valid_card_numbers['visa'])
        sb.type(".p-billing_card_expiry", self.valid_expiry_dates[0])
        sb.type(".p-billing_card_cvc", self.valid_cvc[0])
        sb.wait(1)

    def _verify_payment_history_headers(self, sb):
        """Verify payment history table headers.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
        """
        headers = [
            '.p-billing_payment_date_header',
            '.p-billing_payment_amount_header',
            '.p-billing_payment_status_header'
        ]
        
        for header in headers:
            sb.assert_element_visible(header, timeout=10)

    def _validate_payment_records(self, sb):
        """Validate payment records in the history table.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
        """
        records = sb.find_elements(".p-billing_payment_record")
        if not records:
            raise AssertionError("No payment records found")
            
        for record in records:
            # Verify record has all required fields
            self._validate_payment_record(record)

    def verify_plan_features(self, sb, plan_name):
        """Verify features of a specific plan.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
            plan_name (str): Name of the plan to verify.
            
        Raises:
            AssertionError: If plan features are not as expected.
        """
        plan = self.plan_data[plan_name.lower()]
        
        # Verify plan name and price
        sb.assert_text(plan['name'], f".p-billing_plan_{plan_name.lower()}_name")
        sb.assert_text(plan['price'], f".p-billing_plan_{plan_name.lower()}_price")
        
        # Verify features
        for feature in plan['features']:
            feature_selector = f".p-billing_plan_feature_{feature.lower().replace(' ', '_')}"
            sb.assert_element_visible(feature_selector, timeout=5)
            logger.info(f"Verified feature: {feature} for plan {plan_name}")

    def update_international_address(self, sb, country='uk'):
        """Update billing address with international format.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
            country (str): Country code for address format.
            
        Raises:
            ValueError: If country is not supported.
        """
        if country not in self.valid_addresses:
            raise ValueError(f"Unsupported country: {country}")
            
        address_data = self.valid_addresses[country]
        
        # Click on edit billing info button
        sb.click(".p-billing_edit_button")
        sb.wait(2)
        
        # Update address fields
        self._update_billing_address(sb, address_data)
        
        # Save changes
        sb.click(".p-billing_save_button")
        sb.wait(5)
        
        # Verify success message
        sb.assert_element_visible(".p-billing_success_message", timeout=10)
        sb.assert_text(self.success_messages['address_updated'], ".p-billing_success_message")
        logger.info(f"Updated international address for {country}")

    def verify_network_error_handling(self, sb):
        """Verify handling of network errors during payment processing.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
        """
        # Simulate network error
        sb.execute_script("window.navigator.connection.downlink = 0")
        
        # Try to update payment method
        self._update_payment_method(sb)
        
        # Verify error message
        sb.assert_element_visible(".p-billing_network_error", timeout=10)
        sb.assert_text(self.error_messages['payment_failed'], ".p-billing_network_error")
        logger.info("Verified network error handling")
        
        # Re-enable network
        sb.execute_script("window.navigator.connection.downlink = 10")

    def verify_plan_change_validation(self, sb):
        """Verify validation during plan changes.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
        """
        # Get current plan details
        current_plan = sb.get_text(".p-billing_plan_type")
        current_price = sb.get_text(".p-billing_amount")
        logger.info(f"Current plan: {current_plan}, Price: {current_price}")
        
        # Try to select same plan
        sb.click(".p-billing_change_plan_button")
        sb.wait(2)
        sb.click(f".p-billing_plan_option[data-plan='{current_plan.lower()}']")
        sb.wait(2)
        
        # Verify warning message
        sb.assert_element_visible(".p-billing_plan_warning", timeout=10)
        sb.assert_text("You are already on this plan", ".p-billing_plan_warning")
        
        # Try to select enterprise plan
        sb.click(".p-billing_plan_option[data-plan='enterprise']")
        sb.wait(2)
        
        # Verify permission error
        sb.assert_element_visible(".p-billing_permission_error", timeout=10)
        sb.assert_text("You don't have permission to select this plan", ".p-billing_permission_error")
        logger.info("Verified plan change validation")

    def verify_payment_history_performance(self, sb):
        """Verify performance of payment history loading.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
            
        Returns:
            tuple: (initial_load_time, page_load_time) in seconds
        """
        # Click on payment history tab
        start_time = time.time()
        sb.click(".p-billing_payment_history_tab")
        sb.wait(2)
        
        # Wait for payment history to load
        sb.assert_element_visible(".p-billing_payment_history_table", timeout=10)
        
        initial_load_time = time.time() - start_time
        logger.info(f"Initial payment history load time: {initial_load_time:.2f} seconds")
        
        # Check pagination performance if available
        page_load_time = None
        if sb.is_element_visible(".p-billing_pagination"):
            page_click_start = time.time()
            sb.click(".p-billing_pagination_next")
            sb.wait(2)
            page_load_time = time.time() - page_click_start
            logger.info(f"Page load time: {page_load_time:.2f} seconds")
        
        return initial_load_time, page_load_time

    def verify_invoice_download_validation(self, sb):
        """Verify validation of invoice download functionality.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
        """
        # Click on payment history tab
        sb.click(".p-billing_payment_history_tab")
        sb.wait(2)
        
        # Try to download old invoice
        sb.click(".p-billing_download_invoice_button[data-date='2020-01-01']")
        sb.wait(2)
        
        # Verify error message
        sb.assert_element_visible(".p-billing_download_error", timeout=10)
        sb.assert_text("Invoice not available for this date", ".p-billing_download_error")
        
        # Try to download future invoice
        future_date = (datetime.now().year + 1).__str__()
        sb.click(f".p-billing_download_invoice_button[data-date='{future_date}-01-01']")
        sb.wait(2)
        
        # Verify error message
        sb.assert_element_visible(".p-billing_download_error", timeout=10)
        sb.assert_text("Invalid date for invoice download", ".p-billing_download_error")
        logger.info("Verified invoice download validation")

    def _update_billing_address(self, sb, address_data):
        """Update billing address with provided data.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
            address_data (dict): Address data to use.
        """
        address_fields = {
            '.p-billing_address_input': address_data['street'],
            '.p-billing_city_input': address_data['city'],
            '.p-billing_state_input': address_data['state'],
            '.p-billing_zip_input': address_data['zip'],
            '.p-billing_country_input': address_data['country']
        }
        
        for field, value in address_fields.items():
            sb.type(field, value)
            sb.wait(1) 