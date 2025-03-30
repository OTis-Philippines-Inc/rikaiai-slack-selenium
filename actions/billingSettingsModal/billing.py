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
    INVALID_ADDRESS_DATA, PLAN_DATA, BILLABLE_POINTS_CONFIG,
    ERROR_MESSAGES, SUCCESS_MESSAGES, SUPPORTED_REGIONS,
    UNSUPPORTED_REGIONS
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
        self.points_config = BILLABLE_POINTS_CONFIG
        self.error_messages = ERROR_MESSAGES
        self.success_messages = SUCCESS_MESSAGES
        self.supported_regions = SUPPORTED_REGIONS
        self.unsupported_regions = UNSUPPORTED_REGIONS

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
        
        # Verify points allocation
        points_element = sb.get_element(".p-billing_points")
        points_text = points_element.text
        self._validate_points_format(points_text)
        
        # Verify billing cycle
        sb.assert_element_visible(".p-billing_cycle", timeout=10)
        
        # Verify next billing date
        date_element = sb.get_element(".p-billing_next_date")
        date_text = date_element.text
        self._validate_date_format(date_text)
        
        sb.wait(2)

    def verify_points_usage(self, sb):
        """Verify points usage and breakdown.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
        """
        # Click on points tab
        sb.click(".p-billing_points_tab")
        sb.wait(2)
        
        # Verify points usage table
        sb.assert_element_visible(".p-billing_points_table", timeout=10)
        
        # Verify points breakdown
        sb.assert_element_visible(".p-billing_points_user_messages", timeout=10)
        sb.assert_element_visible(".p-billing_points_translations", timeout=10)
        sb.assert_element_visible(".p-billing_points_edits", timeout=10)
        
        # Verify points rates
        self._verify_points_rates(sb)
        
        sb.wait(2)

    def update_points_limits(self, sb, limit):
        """Update points usage limits.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
            limit (int): The new points limit to set.
        """
        # Click on edit limits button
        sb.click(".p-billing_edit_limits_button")
        sb.wait(2)
        
        # Enter new limit
        sb.type(".p-billing_points_limit_input", str(limit))
        sb.wait(1)
        
        # Save changes
        sb.click(".p-billing_save_limits_button")
        sb.wait(2)
        
        # Verify success message
        sb.assert_element_visible(".p-billing_success_message", timeout=10)
        sb.assert_text(self.success_messages['points_limit_updated'], ".p-billing_success_message")
        
        sb.wait(2)

    def verify_region_validation(self, sb, country):
        """Verify region validation for billing.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
            country (str): The country code to test.
        """
        # Try to update billing info with unsupported region
        self._update_billing_address(sb, {'country': country})
        
        # Verify error message for unsupported region
        sb.assert_element_visible(".p-billing_region_error", timeout=10)
        sb.assert_text(self.error_messages['unsupported_region'], ".p-billing_region_error")
        
        # Update billing info with supported region
        self._update_billing_address(sb, {'country': country})
        
        # Verify success message
        sb.assert_element_visible(".p-billing_success_message", timeout=10)
        sb.assert_text(self.success_messages['address_updated'], ".p-billing_success_message")
        
        sb.wait(2)

    def verify_points_limits(self, sb):
        """Verify points usage limits and warnings.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
        """
        # Click on points tab
        sb.click(".p-billing_points_tab")
        sb.wait(2)
        
        # Verify points limit display
        sb.assert_element_visible(".p-billing_points_limit", timeout=10)
        
        # Verify current usage
        sb.assert_element_visible(".p-billing_points_usage", timeout=10)
        
        # Verify warning if near limit
        if self._is_near_points_limit(sb):
            sb.assert_element_visible(".p-billing_points_warning", timeout=10)
        
        sb.wait(2)

    def _validate_points_format(self, points_text):
        """Validate that the points text follows proper format.
        
        Args:
            points_text (str): The points text to validate.
            
        Raises:
            ValueError: If the points format is invalid.
        """
        points_pattern = r'^\d+(,\d{3})*$'
        if not re.match(points_pattern, points_text):
            raise ValueError(f"Invalid points format: {points_text}")

    def _verify_points_rates(self, sb):
        """Verify points rates for different operations.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
        """
        # Verify user message rate
        sb.assert_text("1.0", ".p-billing_points_user_message_rate")
        
        # Verify first translation rate
        sb.assert_text("0.0", ".p-billing_points_first_translation_rate")
        
        # Verify second translation rate
        sb.assert_text("0.5", ".p-billing_points_second_translation_rate")
        
        # Verify subsequent translations rate
        sb.assert_text("0.25", ".p-billing_points_subsequent_translations_rate")
        
        # Verify edited message rate
        sb.assert_text("0.125", ".p-billing_points_edited_message_rate")

    def _is_near_points_limit(self, sb):
        """Check if points usage is near the limit.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
            
        Returns:
            bool: True if usage is near limit, False otherwise.
        """
        usage = int(sb.get_text(".p-billing_points_usage").replace(",", ""))
        limit = int(sb.get_text(".p-billing_points_limit").replace(",", ""))
        return usage >= limit * 0.9  # 90% of limit

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

    def _update_billing_address(self, sb, address_data=None):
        """Update billing address with validation.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
            address_data (dict, optional): Custom address data to use.
        """
        if address_data is None:
            address_data = {
                'street': '123 Test Street',
                'city': 'Test City',
                'state': 'Test State',
                'zip': '12345',
                'country': 'United States'
            }
        
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

    def _update_payment_method(self, sb):
        """Update payment method with validation.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
        """
        # Select card type
        sb.click(".p-billing_card_type_select")
        sb.wait(1)
        
        # Enter card details
        card_data = self.valid_card_numbers['visa']
        sb.type(".p-billing_card_number_input", card_data['number'])
        sb.type(".p-billing_card_expiry_input", card_data['expiry'])
        sb.type(".p-billing_card_cvc_input", card_data['cvc'])
        
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
        """Validate payment history records.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
        """
        records = sb.find_elements(".p-billing_payment_record")
        
        for record in records:
            # Verify date format
            date_text = record.find_element_by_css_selector(".p-billing_payment_date").text
            self._validate_date_format(date_text)
            
            # Verify amount format
            amount_text = record.find_element_by_css_selector(".p-billing_payment_amount").text
            self._validate_currency_format(amount_text)
            
            # Verify status
            status_text = record.find_element_by_css_selector(".p-billing_payment_status").text
            assert status_text in ['Completed', 'Pending', 'Failed']

    def verify_plan_features(self, sb, plan_name):
        """Verify features for a specific plan.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
            plan_name (str): The name of the plan to verify.
        """
        plan = self.plan_data[plan_name.lower()]
        
        # Verify plan name and price
        sb.assert_text(plan['name'], f".p-billing_plan_{plan_name.lower()}_name")
        sb.assert_text(plan['price'], f".p-billing_plan_{plan_name.lower()}_price")
        
        # Verify features
        for feature in plan['features']:
            feature_selector = f".p-billing_plan_feature_{feature.lower().replace(' ', '_')}"
            sb.assert_element_visible(feature_selector, timeout=10)

    def update_international_address(self, sb, country='uk'):
        """Update billing address with international format.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
            country (str): The country code to use.
        """
        # Get address data for the country
        address_data = self.valid_addresses.get(country.lower())
        if not address_data:
            raise ValueError(f"No valid address data for country: {country}")
        
        # Click on edit billing info button
        sb.click(".p-billing_edit_button")
        sb.wait(2)
        
        # Update address with international format
        self._update_billing_address(sb, address_data)
        
        # Save changes
        sb.click(".p-billing_save_button")
        sb.wait(2)
        
        # Verify success message
        sb.assert_element_visible(".p-billing_success_message", timeout=10)
        sb.assert_text(self.success_messages['address_updated'], ".p-billing_success_message")
        
        sb.wait(2)

    def verify_network_error_handling(self, sb):
        """Verify handling of network errors during billing operations.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
        """
        # Simulate network error
        sb.execute_script("window.navigator.onLine = false;")
        
        # Try to update billing info
        self.update_billing_info(sb)
        
        # Verify error message
        sb.assert_element_visible(".p-billing_network_error", timeout=10)
        sb.assert_text(self.error_messages['payment_failed'], ".p-billing_network_error")
        
        # Restore network connection
        sb.execute_script("window.navigator.onLine = true;")
        
        sb.wait(2)

    def verify_plan_change_validation(self, sb):
        """Verify validation when changing plans.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
        """
        # Get current plan
        current_plan = sb.get_text(".p-billing_plan_type")
        current_price = sb.get_text(".p-billing_amount")
        
        # Try to change to current plan
        sb.click(".p-billing_change_plan_button")
        sb.wait(2)
        sb.click(f".p-billing_plan_option[data-plan='{current_plan.lower()}']")
        sb.wait(2)
        
        # Verify warning message
        sb.assert_element_visible(".p-billing_plan_warning", timeout=10)
        sb.assert_text("You are already on this plan", ".p-billing_plan_warning")
        
        # Try to change to enterprise plan (should fail)
        sb.click(".p-billing_plan_option[data-plan='enterprise']")
        sb.wait(2)
        
        # Verify permission error
        sb.assert_element_visible(".p-billing_permission_error", timeout=10)
        sb.assert_text("You don't have permission to select this plan", ".p-billing_permission_error")
        
        sb.wait(2)

    def verify_payment_history_performance(self, sb):
        """Verify performance of payment history loading.
        
        Args:
            sb (BaseCase): The SeleniumBase test case instance.
        """
        # Click on payment history tab
        sb.click(".p-billing_payment_history_tab")
        sb.wait(2)
        
        # Verify payment history table is visible
        sb.assert_element_visible(".p-billing_payment_history_table", timeout=10)
        
        # Check pagination if present
        if sb.is_element_visible(".p-billing_pagination"):
            # Click next page
            sb.click(".p-billing_pagination_next")
            sb.wait(2)
            
            # Verify next page loaded
            sb.assert_element_visible(".p-billing_payment_history_table", timeout=10)
        
        sb.wait(2)

    def verify_invoice_download_validation(self, sb):
        """Verify validation of invoice download dates.
        
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
        future_date = datetime.now().year + 1
        sb.click(f".p-billing_download_invoice_button[data-date='{future_date}-01-01']")
        sb.wait(2)
        
        # Verify error message
        sb.assert_element_visible(".p-billing_download_error", timeout=10)
        sb.assert_text("Invalid date for invoice download", ".p-billing_download_error")
        
        sb.wait(2) 