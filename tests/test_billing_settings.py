import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seleniumbase import BaseCase
from actions.billingSettingsModal.billing import BillingSettingsModal
from utilities.playback import Playback


class BillingSettingsModalTest(BaseCase):
    def setUp(self):
        super().setUp()
        self.record = Playback(self.driver)

    def test_open_billing_settings(self):
        """Test opening the billing settings modal"""
        self.record.start_recording("test_open_billing_settings")
        BillingSettingsModal().open_billing_settings(self)
        self.record.stop_and_save_recording()
        self.driver.close()

    def test_verify_billing_plan(self):
        """Test verifying billing plan details"""
        self.record.start_recording("test_verify_billing_plan")
        billing = BillingSettingsModal()
        billing.open_billing_settings(self)
        billing.verify_billing_plan(self)
        self.record.stop_and_save_recording()
        self.driver.close()

    def test_update_billing_info(self):
        """Test updating billing information"""
        self.record.start_recording("test_update_billing_info")
        billing = BillingSettingsModal()
        billing.open_billing_settings(self)
        billing.update_billing_info(self)
        self.record.stop_and_save_recording()
        self.driver.close()

    def test_verify_payment_history(self):
        """Test verifying payment history"""
        self.record.start_recording("test_verify_payment_history")
        billing = BillingSettingsModal()
        billing.open_billing_settings(self)
        billing.verify_payment_history(self)
        self.record.stop_and_save_recording()
        self.driver.close()

    def test_change_billing_plan(self):
        """Test changing the billing plan"""
        self.record.start_recording("test_change_billing_plan")
        billing = BillingSettingsModal()
        billing.open_billing_settings(self)
        
        # Click on change plan button
        self.click(".p-billing_change_plan_button")
        self.wait(2)
        
        # Select a new plan
        self.click(".p-billing_plan_option[data-plan='premium']")
        self.wait(2)
        
        # Confirm plan change
        self.click(".p-billing_confirm_plan_change")
        self.wait(5)
        
        # Verify plan change success message
        self.assert_element_visible(".p-billing_plan_change_success", timeout=10)
        
        self.record.stop_and_save_recording()
        self.driver.close()

    def test_download_invoice(self):
        """Test downloading an invoice"""
        self.record.start_recording("test_download_invoice")
        billing = BillingSettingsModal()
        billing.open_billing_settings(self)
        
        # Click on payment history tab
        self.click(".p-billing_payment_history_tab")
        self.wait(2)
        
        # Click download invoice button for the most recent payment
        self.click(".p-billing_download_invoice_button")
        self.wait(5)
        
        # Verify download started
        self.assert_element_visible(".p-billing_download_started", timeout=10)
        
        self.record.stop_and_save_recording()
        self.driver.close()

    def test_cancel_subscription(self):
        """Test canceling subscription"""
        self.record.start_recording("test_cancel_subscription")
        billing = BillingSettingsModal()
        billing.open_billing_settings(self)
        
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
        self.driver.close() 