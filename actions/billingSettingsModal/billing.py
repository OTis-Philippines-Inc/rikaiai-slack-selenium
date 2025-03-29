import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from seleniumbase import BaseCase
from config.settings import settings as cfg


class BillingSettingsModal:
    def open_billing_settings(self, sb):
        """Open the billing settings modal"""
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
        """Verify the current billing plan details"""
        # Verify plan type is visible
        sb.assert_element_visible(".p-billing_plan_type", timeout=10)
        
        # Verify plan details section
        sb.assert_element_visible(".p-billing_plan_details", timeout=10)
        
        # Verify billing amount
        sb.assert_element_visible(".p-billing_amount", timeout=10)
        
        # Verify billing cycle
        sb.assert_element_visible(".p-billing_cycle", timeout=10)
        
        # Verify next billing date
        sb.assert_element_visible(".p-billing_next_date", timeout=10)
        
        sb.wait(2)

    def update_billing_info(self, sb):
        """Update billing information"""
        # Click on edit billing info button
        sb.click(".p-billing_edit_button")
        sb.wait(2)

        # Update billing address
        sb.type(".p-billing_address_input", "123 Test Street")
        sb.type(".p-billing_city_input", "Test City")
        sb.type(".p-billing_state_input", "Test State")
        sb.type(".p-billing_zip_input", "12345")
        sb.type(".p-billing_country_input", "Test Country")
        
        # Update payment method
        sb.click(".p-billing_payment_method_button")
        sb.wait(2)
        sb.type(".p-billing_card_number", "4242424242424242")
        sb.type(".p-billing_card_expiry", "12/25")
        sb.type(".p-billing_card_cvc", "123")
        
        # Save changes
        sb.click(".p-billing_save_button")
        sb.wait(5)
        
        # Verify success message
        sb.assert_element_visible(".p-billing_success_message", timeout=10)
        sb.wait(2)

    def verify_payment_history(self, sb):
        """Verify payment history section"""
        # Click on payment history tab
        sb.click(".p-billing_payment_history_tab")
        sb.wait(2)
        
        # Verify payment history table is visible
        sb.assert_element_visible(".p-billing_payment_history_table", timeout=10)
        
        # Verify table headers
        sb.assert_element_visible(".p-billing_payment_date_header", timeout=10)
        sb.assert_element_visible(".p-billing_payment_amount_header", timeout=10)
        sb.assert_element_visible(".p-billing_payment_status_header", timeout=10)
        
        # Verify at least one payment record exists
        sb.assert_element_visible(".p-billing_payment_record", timeout=10)
        
        sb.wait(2) 