import os
import dotenv

dotenv.load_dotenv()
current_dir = os.path.dirname(os.path.abspath(__file__))


class Settings:
    def __init__(self):
        # General settings
        self.staging_url = os.getenv("STAGING_URL")
        self.gmail = os.getenv("GMAIL")
        self.password = os.getenv("GMAIL_PASSWORD")
        self.staging_name = os.getenv("STAGING_NAME")
        
        # Billing settings
        self.billing_plan = os.getenv("BILLING_PLAN", "basic")
        self.billing_amount = os.getenv("BILLING_AMOUNT", "9.99")
        self.billing_currency = os.getenv("BILLING_CURRENCY", "USD")
        self.billing_cycle = os.getenv("BILLING_CYCLE", "monthly")
        self.billing_status = os.getenv("BILLING_STATUS", "active")
        self.billing_payment_method = os.getenv("BILLING_PAYMENT_METHOD", "card")
        self.billing_card_last4 = os.getenv("BILLING_CARD_LAST4", "4242")
        self.billing_card_brand = os.getenv("BILLING_CARD_BRAND", "visa")
        self.billing_card_expiry = os.getenv("BILLING_CARD_EXPIRY", "12/25")


settings = Settings()
