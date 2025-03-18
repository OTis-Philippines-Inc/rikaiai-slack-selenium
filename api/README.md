# Setting Up Credentials

# Introduction
To automate the login page, Google API is required is needed for this process. To use the API, an intermediate steps are required tocreate the essentials. 

# Step by Step Initialization

## Step 1: Enable the API

Before using Google APIs, we need to enable the API from your account.

1. In the Google Cloud console, enable the Google API you need (e.g., Google Docs API, Google Drive API, etc.).
2. [Enable the API](https://console.cloud.google.com/flows/enableapi?apiid=docs.googleapis.com)

![Enable API](../assets/enable_api.png)

## Step 2: Configure the OAuth Consent Screen

If you're using a new Google Cloud project, you must configure the OAuth consent screen. If you've already completed this step, skip to the next section.

1. In the Google Cloud console, go to **Menu > Google Auth platform > Branding**.
2. [Go to Branding](https://console.cloud.google.com/auth/branding)
3. If you see a message saying "Google Auth platform not configured yet," click **Get Started**.
4. Under **App Information**:
   - In **App name**, enter a name for the app.
   - In **User support email**, choose a support email address where users can contact you if they have questions about their consent.
   - Click **Next**.
5. Under **Audience**:
   - Select **Internal**.
   - Click **Next**.
6. Under **Contact Information**:
   - Enter an **Email address** where you can be notified about any changes to your project.
   - Click **Next**.
7. Under **Finish**:
   - Review the **Google API Services User Data Policy** and, if you agree, select **I agree to the Google API Services: User Data Policy**.
   - Click **Continue**.
   - Click **Create**.
8. For now, you can skip adding scopes. If your app is intended for external users in the future, you must change the **User type** to **External** and add the required authorization scopes.

![Branding](../assets/branding.png)

## Step 3: Authorize Credentials for a Desktop Application

To authenticate end users and access user data in your app, you need to create an **OAuth 2.0 Client ID**. A client ID is used to identify a single app to Google's OAuth servers.

1. In the Google Cloud console, go to **Menu > Google Auth platform > Clients**.
2. [Go to Clients](https://console.cloud.google.com/auth/clients)
3. Click **Create Client**.
4. Select **Application type > Desktop app**.
5. In the **Name** field, type a name for the credential. This name is only shown in the Google Cloud console.
6. Click **Create**.
7. The newly created credential appears under **OAuth 2.0 Client IDs**.
8. Save the downloaded JSON file as **client_secret.json**, and move the file to your working directory.

## Step 4: Add Test Users

For testing purposes, you need to add your email as a test user:

1. Go to **APIs & Services > OAuth consent screen**.
2. Scroll down to the **Test users** section.
3. Click **Add users**, then enter your Gmail address.
4. Click **Save and Continue**.

![Screen Shot of The Process](../assets/add_test_users.png)

## Step 5: Run The script

Move your credentials and rename it as `client_secret.json` to `api/client_secret.json`.
Execute your Python script to authenticate and interact with the Google API.

```bash
python run.py
```

or

```bash
./run.sh
```
## Additional Resources

- [Google API Python Client Documentation](https://developers.google.com/docs/api/quickstart/python)
