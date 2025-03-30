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
        self.billing_plan = os.getenv("BILLING_PLAN", "trial")
        self.billing_amount = os.getenv("BILLING_AMOUNT", "0.00")
        self.billing_currency = os.getenv("BILLING_CURRENCY", "USD")
        self.billing_cycle = os.getenv("BILLING_CYCLE", "monthly")
        self.billing_status = os.getenv("BILLING_STATUS", "active")
        self.billing_payment_method = os.getenv("BILLING_PAYMENT_METHOD", "card")
        self.billing_card_last4 = os.getenv("BILLING_CARD_LAST4", "4242")
        self.billing_card_brand = os.getenv("BILLING_CARD_BRAND", "visa")
        self.billing_card_expiry = os.getenv("BILLING_CARD_EXPIRY", "12/25")
        
        # Billable points settings
        self.billing_points_base = int(os.getenv("BILLING_POINTS_BASE", "50000"))  # Trial plan points
        self.billing_points_additional_cost = float(os.getenv("BILLING_POINTS_ADDITIONAL_COST", "3.99"))  # Cost per 100k additional points
        self.billing_points_overage_rate = float(os.getenv("BILLING_POINTS_OVERAGE_RATE", "0.00004"))  # Rate per point after 1M
        self.billing_points_limit = int(os.getenv("BILLING_POINTS_LIMIT", "50000"))  # Default points limit
        
        # Plan features
        self.billing_available_plans = os.getenv("BILLING_AVAILABLE_PLANS", "trial,paid").split(",")
        self.billing_plan_features = {
            "trial": os.getenv("BILLING_TRIAL_FEATURES", "50k billable points (one-time),Basic support,Parallel translations,Custom language pairs,Basic MTL and LLM-based translations").split(","),
            "paid": os.getenv("BILLING_PAID_FEATURES", "200k billable points base,Priority support,Parallel translations,Custom language pairs,State-of-the-art MTL and LLM-based translations").split(",")
        }
        
        self.billing_plan_prices = {
            "trial": os.getenv("BILLING_TRIAL_PRICE", "0.00"),
            "paid": os.getenv("BILLING_PAID_PRICE", "7.99")
        }
        
        # Region settings
        self.billing_supported_regions = os.getenv("BILLING_SUPPORTED_REGIONS", "US,UK,CA,AU,JP,KR,SG,TW,HK,MY").split(",")
        self.billing_unsupported_regions = os.getenv("BILLING_UNSUPPORTED_REGIONS", "EU,EEA,CN,RU,IR,KP,SY,YE,SO,SS").split(",")
        
        # Performance settings
        self.billing_network_timeout = int(os.getenv("BILLING_NETWORK_TIMEOUT", "30"))
        self.billing_invoice_retention_days = int(os.getenv("BILLING_INVOICE_RETENTION_DAYS", "365"))


settings = Settings()
