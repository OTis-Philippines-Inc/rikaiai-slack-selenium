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
        
        # Additional billing settings
        self.billing_invoice_retention_days = int(os.getenv("BILLING_INVOICE_RETENTION_DAYS", "365"))
        self.billing_max_payment_methods = int(os.getenv("BILLING_MAX_PAYMENT_METHODS", "3"))
        self.billing_available_plans = os.getenv("BILLING_AVAILABLE_PLANS", "basic,premium,enterprise").split(",")
        self.billing_plan_features = {
            "basic": os.getenv("BILLING_BASIC_FEATURES", "Feature 1,Feature 2,Feature 3").split(","),
            "premium": os.getenv("BILLING_PREMIUM_FEATURES", "Feature 1,Feature 2,Feature 3,Feature 4").split(","),
            "enterprise": os.getenv("BILLING_ENTERPRISE_FEATURES", "Feature 1,Feature 2,Feature 3,Feature 4,Feature 5").split(",")
        }
        self.billing_plan_prices = {
            "basic": os.getenv("BILLING_BASIC_PRICE", "9.99"),
            "premium": os.getenv("BILLING_PREMIUM_PRICE", "19.99"),
            "enterprise": os.getenv("BILLING_ENTERPRISE_PRICE", "49.99")
        }
        self.billing_supported_countries = os.getenv("BILLING_SUPPORTED_COUNTRIES", "US,UK,CA,AU").split(",")
        self.billing_network_timeout = int(os.getenv("BILLING_NETWORK_TIMEOUT", "30"))


settings = Settings()
