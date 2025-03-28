# Firebase & Gmail API Setup Guide

This guide explains how to set up and configure the required authentication files for Firebase and Gmail API integration in your Python project.

## Prerequisites
Ensure you have the following installed on your system:
- Python 3.x
- `pip` (Python package manager)
- Google Cloud Project with Gmail API enabled
- Firebase project with Admin SDK enabled

## Required Files
You need to set up the following JSON files inside the `.credentials/` directory:

### 1. `firebase_adminsdk.json`
This file contains the Firebase Admin SDK credentials for authenticating and managing Firebase Authentication.

#### **Setup Steps:**
1. Go to [Firebase Console](https://console.firebase.google.com/).
2. Select your project.
3. Navigate to **Project Settings** > **Service accounts**.
4. Click **Generate new private key**.
5. Download the `.json` file and place it in:
   ```
   .credentials/firebase_adminsdk.json
   ```

### 2. `client_secret.json`
This file contains OAuth credentials for authenticating with the Gmail API.

#### **Setup Steps:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **Gmail API** for your project.
3. Navigate to **APIs & Services** > **Credentials**.
4. Click **Create Credentials** > **OAuth Client ID**.
5. Choose **Desktop App** as the application type.
6. Download the `.json` file and place it in:
   ```
   .credentials/client_secret.json
   ```

### 3. `token.json` (Generated automatically)
This file stores authentication tokens after the first successful login, preventing the need for re-authentication every time the script runs.

#### **How it's created:**
- The first time you run the script, it will prompt you to log in via a browser.
- After authentication, the tokens will be saved in:
  ```
  .credentials/token.json
  ```
- Do **not** manually create this file. It is automatically generated.

## Setting Up the Project

### Install Dependencies
Run the following command to install the required Python packages:
```sh
pip install firebase-admin google-auth google-auth-oauthlib google-auth-httplib2 google-auth google-auth google-api-python-client beautifulsoup4
```

### Environment Structure
Ensure your project structure follows this format:
```
project_root/

│-- .credentials/
│   │-- firebase_adminsdk.json
│   │-- client_secret.json
│   │-- token.json  (auto-generated after login)
│-- actions/loginPage
│   │-- changeSource.py
│   │-- login.py
```

## Running the Script
After setting up the credentials, you can run the script normally:
```sh
sbase gui
```
If it's your first time running the script, a browser window will open for Google authentication. Once authorized, `token.json` will be created and used in future runs.

## Troubleshooting

- **File Not Found Errors:**
  - Ensure that `.credentials/firebase_adminsdk.json` and `.credentials/client_secret.json` exist.
  - Double-check the file paths and names.

- **Invalid Token or Expired Authentication:**
  - Delete `token.json` and re-run the script to re-authenticate.

- **Permission Errors in Gmail API:**
  - Make sure the OAuth client is added to your Google Cloud project and has Gmail API access.
  - Ensure you’ve enabled the correct Gmail API scope (`https://www.googleapis.com/auth/gmail.readonly`).

---
### Need Help?
For more assistance, visit:
- [Firebase Documentation](https://firebase.google.com/docs/admin/setup)
- [Google Gmail API Guide](https://developers.google.com/gmail/api/quickstart/python)

