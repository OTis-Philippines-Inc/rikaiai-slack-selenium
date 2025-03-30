import sys
import os
import pytest
import time
import logging
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seleniumbase import BaseCase
from actions.billingSettingsModal.billing import BillingSettingsModal
from utilities.playback import Playback
from tests.test_data.billing_test_data import (
    VALID_CARD_DATA, VALID_ADDRESS_DATA, INVALID_CARD_DATA,
    INVALID_ADDRESS_DATA, PLAN_DATA, ERROR_MESSAGES, SUCCESS_MESSAGES,
    BILLABLE_POINTS_CONFIG, SUPPORTED_REGIONS, UNSUPPORTED_REGIONS
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BillingSettingsModalTest(BaseCase):
    """Test suite for the Billing Settings Modal functionality.
    
    This test suite covers all major functionality of the billing settings modal,
    including plan management, payment information updates, and payment history.
    """

    @classmethod
    def setUpClass(cls):
        """Set up test class with common test data."""
        super().setUpClass()
        cls.billing = BillingSettingsModal()
        logger.info("Starting Billing Settings Modal Test Suite")

    def setUp(self):
        """Set up each test case."""
        super().setUp()
        self.record = Playback(self.driver)
        self.start_time = time.time()
        logger.info(f"Starting test: {self._testMethodName}")

    def tearDown(self):
        """Clean up after each test case."""
        duration = time.time() - self.start_time
        logger.info(f"Test {self._testMethodName} completed in {duration:.2f} seconds")
        self.driver.close()
        super().tearDown()

    @pytest.mark.basic
    def test_open_billing_settings(self):
        """Test opening the billing settings modal.
        
        Category: Basic Functionality
        """
        self.record.start_recording("test_open_billing_settings")
        self.billing.open_billing_settings(self)
        self.record.stop_and_save_recording()

    @pytest.mark.basic
    def test_verify_billing_plan(self):
        """Test verifying billing plan details.
        
        Category: Basic Functionality
        """
        self.record.start_recording("test_verify_billing_plan")
        self.billing.open_billing_settings(self)
        self.billing.verify_billing_plan(self)
        self.record.stop_and_save_recording()

    @pytest.mark.payment
    def test_update_billing_info(self):
        """Test updating billing information.
        
        Category: Payment Management
        """
        self.record.start_recording("test_update_billing_info")
        self.billing.open_billing_settings(self)
        self.billing.update_billing_info(self)
        self.record.stop_and_save_recording()

    @pytest.mark.payment
    def test_verify_payment_history(self):
        """Test verifying payment history.
        
        Category: Payment Management
        """
        self.record.start_recording("test_verify_payment_history")
        self.billing.open_billing_settings(self)
        self.billing.verify_payment_history(self)
        self.record.stop_and_save_recording()

    @pytest.mark.plan
    def test_change_billing_plan(self):
        """Test changing the billing plan.
        
        Category: Plan Management
        """
        self.record.start_recording("test_change_billing_plan")
        self.billing.open_billing_settings(self)
        
        # Click on change plan button
        self.click(".p-billing_change_plan_button")
        self.wait(2)
        
        # Select paid plan
        self.click(".p-billing_plan_option[data-plan='paid']")
        self.wait(2)
        
        # Confirm plan change
        self.click(".p-billing_confirm_plan_change")
        self.wait(5)
        
        # Verify plan change success message
        self.assert_element_visible(".p-billing_plan_change_success", timeout=10)
        
        self.record.stop_and_save_recording()

    @pytest.mark.payment
    def test_download_invoice(self):
        """Test downloading an invoice.
        
        Category: Payment Management
        """
        self.record.start_recording("test_download_invoice")
        self.billing.open_billing_settings(self)
        
        # Click on payment history tab
        self.click(".p-billing_payment_history_tab")
        self.wait(2)
        
        # Click download invoice button for the most recent payment
        self.click(".p-billing_download_invoice_button")
        self.wait(5)
        
        # Verify download started
        self.assert_element_visible(".p-billing_download_started", timeout=10)
        
        self.record.stop_and_save_recording()

    @pytest.mark.plan
    def test_cancel_subscription(self):
        """Test canceling subscription.
        
        Category: Plan Management
        """
        self.record.start_recording("test_cancel_subscription")
        self.billing.open_billing_settings(self)
        
        # Click on cancel subscription button
        self.click(".p-billing_cancel_subscription_button")
        self.wait(2)
        
        # Select cancellation reason
        self.click(".p-billing_cancellation_reason[data-reason='too_expensive']")
        self.wait(2)
        
        # Enter feedback
        self.type(".p-billing_cancellation_feedback", "Test cancellation feedback")
        self.wait(2)
        
        # Confirm cancellation
        self.click(".p-billing_confirm_cancellation")
        self.wait(5)
        
        # Verify cancellation success message
        self.assert_element_visible(".p-billing_cancellation_success", timeout=10)
        
        self.record.stop_and_save_recording()

    @pytest.mark.error
    def test_invalid_card_number(self):
        """Test handling of invalid card number.
        
        Category: Error Handling
        """
        self.record.start_recording("test_invalid_card_number")
        self.billing.open_billing_settings(self)
        
        # Click on edit billing info button
        self.click(".p-billing_edit_button")
        self.wait(2)
        
        # Click on payment method button
        self.click(".p-billing_payment_method_button")
        self.wait(2)
        
        # Enter invalid card number
        self.type(".p-billing_card_number", "1234567890123456")
        self.wait(2)
        
        # Verify error message
        self.assert_element_visible(".p-billing_card_error", timeout=10)
        
        self.record.stop_and_save_recording()

    @pytest.mark.error
    def test_expired_card(self):
        """Test handling of expired card.
        
        Category: Error Handling
        """
        self.record.start_recording("test_expired_card")
        self.billing.open_billing_settings(self)
        
        # Click on edit billing info button
        self.click(".p-billing_edit_button")
        self.wait(2)
        
        # Click on payment method button
        self.click(".p-billing_payment_method_button")
        self.wait(2)
        
        # Enter expired card details
        self.type(".p-billing_card_number", "4242424242424242")
        self.type(".p-billing_card_expiry", "01/20")
        self.type(".p-billing_card_cvc", "123")
        self.wait(2)
        
        # Verify error message
        self.assert_element_visible(".p-billing_card_expired_error", timeout=10)
        
        self.record.stop_and_save_recording()

    @pytest.mark.error
    def test_invalid_billing_address(self):
        """Test handling of invalid billing address.
        
        Category: Error Handling
        """
        self.record.start_recording("test_invalid_billing_address")
        self.billing.open_billing_settings(self)
        
        # Click on edit billing info button
        self.click(".p-billing_edit_button")
        self.wait(2)
        
        # Enter invalid zip code
        self.type(".p-billing_zip_input", "123")
        self.wait(2)
        
        # Verify error message
        self.assert_element_visible(".p-billing_zip_error", timeout=10)
        
        self.record.stop_and_save_recording()

    @pytest.mark.plan
    def test_plan_upgrade_downgrade(self):
        """Test upgrading and downgrading between plans.
        
        Category: Plan Management
        """
        self.record.start_recording("test_plan_upgrade_downgrade")
        self.billing.open_billing_settings(self)
        
        # Start with trial plan
        self.assert_text("Trial Plan", ".p-billing_plan_type")
        
        # Upgrade to paid plan
        self.click(".p-billing_change_plan_button")
        self.wait(2)
        self.click(".p-billing_plan_option[data-plan='paid']")
        self.wait(2)
        self.click(".p-billing_confirm_plan_change")
        self.wait(5)
        
        # Verify upgrade success
        self.assert_text("Paid Plan", ".p-billing_plan_type")
        
        # Downgrade back to trial
        self.click(".p-billing_change_plan_button")
        self.wait(2)
        self.click(".p-billing_plan_option[data-plan='trial']")
        self.wait(2)
        self.click(".p-billing_confirm_plan_change")
        self.wait(5)
        
        # Verify downgrade success
        self.assert_text("Trial Plan", ".p-billing_plan_type")
        
        self.record.stop_and_save_recording()

    @pytest.mark.payment
    def test_multiple_payment_methods(self):
        """Test managing multiple payment methods.
        
        Category: Payment Management
        """
        self.record.start_recording("test_multiple_payment_methods")
        self.billing.open_billing_settings(self)
        
        # Add first payment method
        self.click(".p-billing_add_payment_method")
        self.wait(2)
        self.type(".p-billing_card_number", "4242424242424242")
        self.type(".p-billing_card_expiry", "12/25")
        self.type(".p-billing_card_cvc", "123")
        self.click(".p-billing_save_card")
        self.wait(5)
        
        # Add second payment method
        self.click(".p-billing_add_payment_method")
        self.wait(2)
        self.type(".p-billing_card_number", "5555555555554444")
        self.type(".p-billing_card_expiry", "01/26")
        self.type(".p-billing_card_cvc", "456")
        self.click(".p-billing_save_card")
        self.wait(5)
        
        # Verify both cards are listed
        self.assert_element_visible(".p-billing_card_list", timeout=10)
        self.assert_element_visible(".p-billing_card_item:nth-child(1)", timeout=10)
        self.assert_element_visible(".p-billing_card_item:nth-child(2)", timeout=10)
        
        self.record.stop_and_save_recording()

    @pytest.mark.performance
    def test_modal_load_time(self):
        """Test the performance of modal loading.
        
        Category: Performance
        """
        self.record.start_recording("test_modal_load_time")
        start_time = time.time()
        
        self.billing.open_billing_settings(self)
        
        load_time = time.time() - start_time
        logger.info(f"Modal load time: {load_time:.2f} seconds")
        
        # Assert load time is within acceptable range (e.g., 5 seconds)
        assert load_time < 5, f"Modal load time ({load_time:.2f}s) exceeded threshold"
        
        self.record.stop_and_save_recording()

    @pytest.mark.validation
    def test_plan_feature_comparison(self):
        """Test comparing features between different plans.
        
        Category: Validation
        """
        self.record.start_recording("test_plan_feature_comparison")
        self.billing.open_billing_settings(self)
        
        # Click on plan comparison button
        self.click(".p-billing_compare_plans_button")
        self.wait(2)
        
        # Verify all plans are displayed
        for plan in PLAN_DATA.values():
            self.assert_element_visible(f".p-billing_plan_{plan['name'].lower().replace(' ', '_')}", timeout=10)
            self.assert_text(plan['price'], f".p-billing_plan_{plan['name'].lower().replace(' ', '_')}_price")
            
            # Verify features
            for feature in plan['features']:
                self.assert_element_visible(f".p-billing_plan_feature_{feature.lower().replace(' ', '_')}", timeout=5)
        
        self.record.stop_and_save_recording()

    @pytest.mark.validation
    def test_international_billing_address(self):
        """Test handling of international billing addresses.
        
        Category: Validation
        """
        self.record.start_recording("test_international_billing_address")
        self.billing.open_billing_settings(self)
        
        # Click on edit billing info button
        self.click(".p-billing_edit_button")
        self.wait(2)
        
        # Test UK address
        uk_address = VALID_ADDRESS_DATA['uk']
        self.type(".p-billing_address_input", uk_address['street'])
        self.type(".p-billing_city_input", uk_address['city'])
        self.type(".p-billing_state_input", uk_address['state'])
        self.type(".p-billing_zip_input", uk_address['zip'])
        self.type(".p-billing_country_input", uk_address['country'])
        
        # Save changes
        self.click(".p-billing_save_button")
        self.wait(5)
        
        # Verify success message
        self.assert_element_visible(".p-billing_success_message", timeout=10)
        self.assert_text(SUCCESS_MESSAGES['address_updated'], ".p-billing_success_message")
        
        self.record.stop_and_save_recording()

    @pytest.mark.error
    def test_network_error_handling(self):
        """Test handling of network errors during payment processing.
        
        Category: Error Handling
        """
        self.record.start_recording("test_network_error_handling")
        self.billing.open_billing_settings(self)
        
        # Click on edit billing info button
        self.click(".p-billing_edit_button")
        self.wait(2)
        
        # Simulate network error by disabling network
        self.execute_script("window.navigator.connection.downlink = 0")
        
        # Try to update payment method
        self.click(".p-billing_payment_method_button")
        self.wait(2)
        
        # Enter valid card details
        card_data = VALID_CARD_DATA['visa']
        self.type(".p-billing_card_number", card_data['number'])
        self.type(".p-billing_card_expiry", card_data['expiry'])
        self.type(".p-billing_card_cvc", card_data['cvc'])
        
        # Try to save
        self.click(".p-billing_save_card")
        self.wait(5)
        
        # Verify error message
        self.assert_element_visible(".p-billing_network_error", timeout=10)
        self.assert_text(ERROR_MESSAGES['payment_failed'], ".p-billing_network_error")
        
        # Re-enable network
        self.execute_script("window.navigator.connection.downlink = 10")
        
        self.record.stop_and_save_recording()

    @pytest.mark.validation
    def test_plan_change_validation(self):
        """Test validation during plan changes.
        
        Category: Validation
        """
        self.record.start_recording("test_plan_change_validation")
        self.billing.open_billing_settings(self)
        
        # Get current plan details
        current_plan = self.get_text(".p-billing_plan_type")
        current_price = self.get_text(".p-billing_amount")
        
        # Click on change plan button
        self.click(".p-billing_change_plan_button")
        self.wait(2)
        
        # Try to select same plan
        self.click(f".p-billing_plan_option[data-plan='{current_plan.lower()}']")
        self.wait(2)
        
        # Verify warning message
        self.assert_element_visible(".p-billing_plan_warning", timeout=10)
        self.assert_text("You are already on this plan", ".p-billing_plan_warning")
        
        # Try to select enterprise plan without proper permissions
        self.click(".p-billing_plan_option[data-plan='enterprise']")
        self.wait(2)
        
        # Verify permission error
        self.assert_element_visible(".p-billing_permission_error", timeout=10)
        self.assert_text("You don't have permission to select this plan", ".p-billing_permission_error")
        
        self.record.stop_and_save_recording()

    @pytest.mark.performance
    def test_payment_history_load_time(self):
        """Test the performance of payment history loading.
        
        Category: Performance
        """
        self.record.start_recording("test_payment_history_load_time")
        self.billing.open_billing_settings(self)
        
        # Click on payment history tab
        start_time = time.time()
        self.click(".p-billing_payment_history_tab")
        self.wait(2)
        
        # Wait for payment history to load
        self.assert_element_visible(".p-billing_payment_history_table", timeout=10)
        
        load_time = time.time() - start_time
        logger.info(f"Payment history load time: {load_time:.2f} seconds")
        
        # Assert load time is within acceptable range (e.g., 3 seconds)
        assert load_time < 3, f"Payment history load time ({load_time:.2f}s) exceeded threshold"
        
        # Verify pagination performance
        if self.is_element_visible(".p-billing_pagination"):
            page_click_start = time.time()
            self.click(".p-billing_pagination_next")
            self.wait(2)
            page_load_time = time.time() - page_click_start
            logger.info(f"Page load time: {page_load_time:.2f} seconds")
            assert page_load_time < 2, f"Page load time ({page_load_time:.2f}s) exceeded threshold"
        
        self.record.stop_and_save_recording()

    @pytest.mark.validation
    def test_invoice_download_validation(self):
        """Test validation of invoice download functionality.
        
        Category: Validation
        """
        self.record.start_recording("test_invoice_download_validation")
        self.billing.open_billing_settings(self)
        
        # Click on payment history tab
        self.click(".p-billing_payment_history_tab")
        self.wait(2)
        
        # Try to download invoice for a very old payment
        self.click(".p-billing_download_invoice_button[data-date='2020-01-01']")
        self.wait(2)
        
        # Verify error message
        self.assert_element_visible(".p-billing_download_error", timeout=10)
        self.assert_text("Invoice not available for this date", ".p-billing_download_error")
        
        # Try to download invoice for future date
        future_date = (datetime.now().year + 1).__str__()
        self.click(f".p-billing_download_invoice_button[data-date='{future_date}-01-01']")
        self.wait(2)
        
        # Verify error message
        self.assert_element_visible(".p-billing_download_error", timeout=10)
        self.assert_text("Invalid date for invoice download", ".p-billing_download_error")
        
        self.record.stop_and_save_recording()

    @pytest.mark.points
    def test_verify_points_usage(self):
        """Test verifying billable points usage.
        
        Category: Points Management
        """
        self.record.start_recording("test_verify_points_usage")
        self.billing.open_billing_settings(self)
        self.billing.verify_points_usage(self)
        self.record.stop_and_save_recording()

    @pytest.mark.points
    def test_update_points_limits(self):
        """Test updating billable points limits.
        
        Category: Points Management
        """
        self.record.start_recording("test_update_points_limits")
        self.billing.open_billing_settings(self)
        
        # Update to a new limit
        self.billing.update_points_limits(self, 100000)
        self.wait(2)
        
        # Verify the new limit is displayed
        self.assert_text("100,000", ".p-billing_points_limit")
        
        self.record.stop_and_save_recording()

    @pytest.mark.points
    def test_points_limit_warning(self):
        """Test points limit warning display.
        
        Category: Points Management
        """
        self.record.start_recording("test_points_limit_warning")
        self.billing.open_billing_settings(self)
        
        # Set a low limit
        self.billing.update_points_limits(self, 1000)
        self.wait(2)
        
        # Simulate high usage
        self.execute_script("document.querySelector('.p-billing_points_usage').textContent = '950'")
        self.wait(2)
        
        # Verify warning is displayed
        self.assert_element_visible(".p-billing_points_warning", timeout=10)
        
        self.record.stop_and_save_recording()

    @pytest.mark.region
    def test_region_validation(self):
        """Test region validation for billing.
        
        Category: Region Validation
        """
        self.record.start_recording("test_region_validation")
        self.billing.open_billing_settings(self)
        
        # Test supported region
        self.billing.verify_region_validation(self, "US")
        self.wait(2)
        
        # Test unsupported region
        self.billing.verify_region_validation(self, "CN")
        self.wait(2)
        
        self.record.stop_and_save_recording()

    @pytest.mark.plan
    def test_plan_upgrade_to_paid(self):
        """Test upgrading from trial to paid plan.
        
        Category: Plan Management
        """
        self.record.start_recording("test_plan_upgrade_to_paid")
        self.billing.open_billing_settings(self)
        
        # Verify starting on trial plan
        self.assert_text("Trial Plan", ".p-billing_plan_type")
        
        # Upgrade to paid plan
        self.click(".p-billing_change_plan_button")
        self.wait(2)
        self.click(".p-billing_plan_option[data-plan='paid']")
        self.wait(2)
        
        # Verify plan details
        self.assert_text("$7.99", ".p-billing_plan_price")
        self.assert_text("200k billable points base", ".p-billing_plan_features")
        
        # Confirm upgrade
        self.click(".p-billing_confirm_plan_change")
        self.wait(5)
        
        # Verify upgrade success
        self.assert_text("Paid Plan", ".p-billing_plan_type")
        self.assert_text("$7.99", ".p-billing_amount")
        
        self.record.stop_and_save_recording()

    @pytest.mark.points
    def test_points_calculation(self):
        """Test billable points calculation.
        
        Category: Points Management
        """
        self.record.start_recording("test_points_calculation")
        self.billing.open_billing_settings(self)
        
        # Click on points usage tab
        self.click(".p-billing_points_tab")
        self.wait(2)
        
        # Verify points breakdown
        self.assert_element_visible(".p-billing_points_user_messages", timeout=10)
        self.assert_element_visible(".p-billing_points_translations", timeout=10)
        self.assert_element_visible(".p-billing_points_edits", timeout=10)
        
        # Verify points rates
        self.assert_text("1.0", ".p-billing_points_rate_user")
        self.assert_text("0.5", ".p-billing_points_rate_second")
        self.assert_text("0.25", ".p-billing_points_rate_subsequent")
        self.assert_text("0.125", ".p-billing_points_rate_edit")
        
        self.record.stop_and_save_recording()

    @pytest.mark.payment
    def test_payment_with_points_limit(self):
        """Test payment processing with points limit.
        
        Category: Payment Management
        """
        self.record.start_recording("test_payment_with_points_limit")
        self.billing.open_billing_settings(self)
        
        # Set a points limit
        self.billing.update_points_limits(self, 1000)
        self.wait(2)
        
        # Try to process payment
        self.click(".p-billing_process_payment_button")
        self.wait(2)
        
        # Verify points limit check
        self.assert_element_visible(".p-billing_points_limit_check", timeout=10)
        
        self.record.stop_and_save_recording() 