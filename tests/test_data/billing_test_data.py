"""Test data for billing settings tests."""

# Valid test data
VALID_CARD_DATA = {
    'visa': {
        'number': '4242424242424242',
        'expiry': '12/25',
        'cvc': '123',
        'brand': 'Visa'
    },
    'mastercard': {
        'number': '5555555555554444',
        'expiry': '01/26',
        'cvc': '456',
        'brand': 'Mastercard'
    },
    'amex': {
        'number': '378282246310005',
        'expiry': '06/24',
        'cvc': '789',
        'brand': 'American Express'
    }
}

VALID_ADDRESS_DATA = {
    'us': {
        'street': '123 Test Street',
        'city': 'Test City',
        'state': 'Test State',
        'zip': '12345',
        'country': 'United States'
    },
    'uk': {
        'street': '456 Test Road',
        'city': 'Test Town',
        'state': 'Test County',
        'zip': 'TE1 1ST',
        'country': 'United Kingdom'
    }
}

# Invalid test data
INVALID_CARD_DATA = {
    'invalid_number': {
        'number': '1234567890123456',
        'expiry': '12/25',
        'cvc': '123'
    },
    'expired': {
        'number': '4242424242424242',
        'expiry': '01/20',
        'cvc': '123'
    },
    'invalid_cvc': {
        'number': '4242424242424242',
        'expiry': '12/25',
        'cvc': '12'
    }
}

INVALID_ADDRESS_DATA = {
    'invalid_zip': {
        'street': '123 Test Street',
        'city': 'Test City',
        'state': 'Test State',
        'zip': '123',
        'country': 'United States'
    },
    'missing_fields': {
        'street': '123 Test Street',
        'city': 'Test City',
        'zip': '12345'
    }
}

# Plan data
PLAN_DATA = {
    'trial': {
        'name': 'Trial Plan',
        'price': 'FREE',
        'features': [
            '50k billable points (one-time)',
            'Basic support',
            'Parallel translations',
            'Custom language pairs',
            'Basic MTL and LLM-based translations'
        ]
    },
    'paid': {
        'name': 'Paid Plan',
        'price': '$7.99',
        'features': [
            '200k billable points base',
            'Priority support',
            'Parallel translations',
            'Custom language pairs',
            'State-of-the-art MTL and LLM-based translations',
            '$3.99 per 100k additional points',
            '$0.04 per 1000 points after 1M points'
        ]
    }
}

# Billable points configuration
BILLABLE_POINTS_CONFIG = {
    'user_message': 1.0,
    'first_translation': 0.0,
    'second_translation': 0.5,
    'subsequent_translations': 0.25,
    'edited_message': 0.125
}

# Error messages
ERROR_MESSAGES = {
    'invalid_card': 'Invalid card number',
    'expired_card': 'Card has expired',
    'invalid_cvc': 'Invalid CVC',
    'invalid_zip': 'Invalid ZIP code',
    'missing_fields': 'Please fill in all required fields',
    'payment_failed': 'Payment processing failed',
    'plan_change_failed': 'Failed to change plan',
    'points_limit_exceeded': 'Translation limit exceeded',
    'unsupported_region': 'Service not available in your region'
}

# Success messages
SUCCESS_MESSAGES = {
    'card_added': 'Card added successfully',
    'card_updated': 'Card updated successfully',
    'address_updated': 'Address updated successfully',
    'plan_changed': 'Plan changed successfully',
    'subscription_cancelled': 'Subscription cancelled successfully',
    'points_limit_updated': 'Translation limits updated successfully'
}

# Supported regions
SUPPORTED_REGIONS = [
    'US', 'UK', 'CA', 'AU', 'JP', 'KR', 'SG', 'TW', 'HK', 'MY'
]

# Unsupported regions
UNSUPPORTED_REGIONS = [
    'EU', 'EEA', 'CN', 'RU', 'IR', 'KP', 'SY', 'YE', 'SO', 'SS'
] 