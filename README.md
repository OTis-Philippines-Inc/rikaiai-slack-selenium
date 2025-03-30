# RIKAIAI Slack Selenium Testing

This repository contains automated tests for the RIKAIAI Slack application, focusing on billing settings functionality.

## Billing Settings Implementation

The billing settings implementation includes comprehensive testing for RIKAIAI's points-based billing system.

### Features

1. **Plan Management**
   - Trial Plan (Free)
     - 50k billable points (one-time)
     - Basic support
     - Parallel translations
     - Custom language pairs
     - Basic MTL and LLM-based translations
   
   - Paid Plan ($7.99/month)
     - 200k billable points base
     - Priority support
     - Parallel translations
     - Custom language pairs
     - State-of-the-art MTL and LLM-based translations
     - $3.99 per 100k additional points
     - $0.04 per 1000 points after 1M points

2. **Points System**
   - Points calculation based on usage:
     - User messages: 1.0 point
     - First translation: 0.0 points
     - Second translation: 0.5 points
     - Subsequent translations: 0.25 points
     - Edited messages: 0.125 points

3. **Regional Availability**
   - Supported Regions: US, UK, CA, AU, JP, KR, SG, TW, HK, MY
   - Unsupported Regions: EU, EEA, CN, RU, IR, KP, SY, YE, SO, SS

4. **Payment Management**
   - Multiple payment method support
   - International billing addresses
   - Invoice generation and download
   - Payment history tracking

### Test Coverage

The test suite covers:

1. **Basic Functionality**
   - Opening billing settings
   - Verifying billing plan details
   - Checking points usage and limits

2. **Payment Management**
   - Updating billing information
   - Verifying payment history
   - Downloading invoices
   - Handling multiple payment methods

3. **Plan Management**
   - Upgrading from trial to paid plan
   - Downgrading between plans
   - Plan feature comparison
   - Subscription cancellation

4. **Error Handling**
   - Invalid card numbers
   - Expired cards
   - Invalid billing addresses
   - Network errors
   - Region validation

5. **Performance**
   - Modal load time
   - Payment history load time
   - Network timeout handling

### Configuration

The billing settings are configured through environment variables in `.env`:

```env
# Billing settings
BILLING_PLAN = "trial"
BILLING_AMOUNT = "0.00"
BILLING_CURRENCY = "USD"
BILLING_CYCLE = "monthly"

# Billable points settings
BILLING_POINTS_BASE = "50000"
BILLING_POINTS_ADDITIONAL_COST = "3.99"
BILLING_POINTS_OVERAGE_RATE = "0.00004"
BILLING_POINTS_LIMIT = "50000"

# Region settings
BILLING_SUPPORTED_REGIONS = "US,UK,CA,AU,JP,KR,SG,TW,HK,MY"
BILLING_UNSUPPORTED_REGIONS = "EU,EEA,CN,RU,IR,KP,SY,YE,SO,SS"
```

### Running Tests

To run the billing settings tests:

```bash
# Run all billing tests
pytest tests/test_billing_settings.py

# Run specific test categories
pytest tests/test_billing_settings.py -m basic
pytest tests/test_billing_settings.py -m payment
pytest tests/test_billing_settings.py -m plan
pytest tests/test_billing_settings.py -m points
pytest tests/test_billing_settings.py -m region
```

## Important note
All instructions below assume that you are working within the parent repository located at `/rikaiai-slack-selenium` on your local machine.

## Setting up the environment
1. Open a terminal and navigate to the root directory of the project.
`rikaiai-slack-selenium/`
2. Create a virtual environment by running the following command:
```sh
python -m venv .venv
```
3. Activate the virtual environment:
On Windows, run:
```sh
source rikaiai-slack-selenium-venv/Scripts/activate
```
On macOS and Linux, run:
```sh 
source rikaiai-slack-selenium-venv/bin/activate
```
4. Install the required dependencies by running the following command:
```sh
pip install -r requirements.txt
```

## Running the automation testing scripts

### Using `sbase` by Seleniumbase
1. In your terminal, ensure you are in the `rikaiai-slack-selenium/` directory before running the following command:
```sh
sbase gui
```

### Using Shell Scripts
In the parent directory `rikaiai-slack-selenium/`, run this command;
- On Windows, run:
```sh
./win-start.sh
```
- On macOS and Linux, run:
```sh 
./start.sh 
```