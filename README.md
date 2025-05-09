# Gmail Email Cleanup Script

This Python script is designed to help clean up your Gmail inbox by automatically unsubscribing from unwanted email lists and deleting **every** email in your inbox. The script processes **all** emails, not just selective ones (like spam or promotions), and utilizes multi-threading to speed up the process. It also gives you the option to control the number of threads used.

## Features

- **Unsubscribe from Email Lists**: The script attempts to unsubscribe from emails that have a `List-Unsubscribe` header.
- **Delete All Emails**: After unsubscribing (if applicable), the script deletes all emails in the inbox.
- **Multi-threading**: The script processes emails using multiple threads, allowing for faster cleanup. You can adjust the number of threads if needed.
- **Summary**: After the script completes, it outputs a summary showing how many emails were unsubscribed from and how many were deleted.

## Prerequisites

- Python 3.6 or higher
- An active Gmail account
- An app-specific password for Gmail

## Installation

### Step 1: Install Python

If you don’t have Python installed, follow these steps:
1. Download and install Python from [python.org](https://www.python.org/downloads/).
2. Make sure to check the option to "Add Python to PATH" during installation.

### Step 2: Install Required Libraries

This script uses the `requests` library. To install it, open a terminal or command prompt and run:

```bash
pip install requests

Step 3: Set Up Gmail Access

To use this script with Gmail, you must create an app-specific password. Follow these steps:

    Enable 2-Step Verification for your Gmail account:

        Go to Google Account Settings.

        Under the Security tab, enable 2-Step Verification if you haven’t already.

    Create an App-Specific Password:

        In the Security section of your Google Account, find App passwords (this option will only appear if 2-Step Verification is enabled).

        Select Mail as the app and Windows Computer as the device.

        Click Generate to create an app-specific password.

        Copy the password (you will need it for the script).

Step 4: Update the Script with Your Credentials

    Open the script in a text editor (e.g., Notepad++ or Visual Studio Code).

    Replace the EMAIL and PASSWORD placeholders with your Gmail address and the app-specific password:

    EMAIL = "your-email@gmail.com"
    PASSWORD = "your-app-password"

Step 5: Adjust Threading (Optional)

You can modify the number of threads used for processing emails in parallel by changing the MAX_WORKERS value.

    Find the line MAX_WORKERS = 10.

    Modify it to any number you prefer (e.g., MAX_WORKERS = 5 to use 5 threads).

    Save the script with the new value.

Step 6: Run the Script

    Open Command Prompt (Windows) or Terminal (macOS/Linux).

    Navigate to the folder where the script is saved.

    Run the script using the following command:

    python cleanup_script.py

The script will start processing your inbox. It will attempt to unsubscribe from any email lists and then delete every email in your inbox. Once finished, the script will output a summary of how many emails were unsubscribed from and deleted.
How the Script Works

    IMAP Connection: The script connects to Gmail’s IMAP server (imap.gmail.com) using your Gmail credentials and accesses your inbox remotely.

    Email Fetching: It fetches all email IDs in the inbox and processes them in chunks, using multi-threading for faster execution.

    Unsubscribing: The script looks for a List-Unsubscribe header in each email and attempts to unsubscribe using the URL in the header.

    Deleting All Emails: After attempting to unsubscribe (if applicable), the script deletes every email from your inbox.

    Multi-threading: The emails are processed in parallel using ThreadPoolExecutor. You can control the number of threads used by modifying the MAX_WORKERS variable.

Adjusting Thread Count

You can adjust the number of threads by changing the MAX_WORKERS value in the script:

MAX_WORKERS = 10  # Default is 10 threads

To use more threads (e.g., 5 threads):

MAX_WORKERS = 5

Example Usage:

python cleanup_script.py

Troubleshooting

    IMAP Login Issues: If you have trouble logging in, ensure you’ve enabled IMAP in your Gmail settings and that you’re using an app-specific password.

    Unsubscribe Failures: If the unsubscribe attempt fails, it may be due to an invalid or missing unsubscribe URL in the email header.

    Email Deletion Not Working: Double-check that you have proper IMAP settings enabled in Gmail.

License

This project is licensed under the MIT License - see the LICENSE file for details.

Feel free to fork and modify this script for your needs. Enjoy your cleaner inbox!
