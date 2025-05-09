import imaplib
import email
import requests
import re
from email.header import decode_header
from concurrent.futures import ThreadPoolExecutor

# === CONFIG ===
EMAIL = "your-email@gmail.com"  # Replace with your email
PASSWORD = "your-app-password"  # Replace with your app password
IMAP_SERVER = "imap.gmail.com"
MAX_WORKERS = 10

unsubscribe_count = 0
delete_count = 0

# === Attempt to unsubscribe from a URL ===
def attempt_unsubscribe(unsubscribe_url):
    global unsubscribe_count
    try:
        if unsubscribe_url.startswith("<") and unsubscribe_url.endswith(">"):
            unsubscribe_url = unsubscribe_url[1:-1]
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(unsubscribe_url, headers=headers)
        if response.status_code == 200:
            print(f"✅ Unsubscribed from: {unsubscribe_url}")
            unsubscribe_count += 1
        else:
            print(f"❌ Failed unsubscribe (status {response.status_code}): {unsubscribe_url}")
    except Exception as e:
        print(f"⚠️ Error unsubscribing: {e}")

# === Process a batch of email IDs ===
def process_chunk(email_ids_chunk):
    global delete_count
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")

        for email_id in email_ids_chunk:
            try:
                status, msg_data = mail.fetch(email_id, "(BODY.PEEK[HEADER])")
                if status != "OK":
                    continue

                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8")

                        # Attempt to unsubscribe if a List-Unsubscribe header exists
                        unsubscribe_header = msg.get("List-Unsubscribe")
                        if unsubscribe_header:
                            urls = re.findall(r'<(http[s]?://[^>]+)>', unsubscribe_header)
                            for url in urls:
                                attempt_unsubscribe(url)
                                break  # Only one per email

                        # Delete the email
                        print(f"🗑️ Deleting: {subject}")
                        mail.store(email_id, '+FLAGS', '\\Deleted')
                        delete_count += 1

            except Exception as e:
                print(f"Error processing email {email_id}: {e}")

        mail.expunge()
        mail.logout()
    except Exception as e:
        print(f"Thread-level error: {e}")

# === Fetch all email IDs from inbox ===
def get_all_email_ids():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")
    status, messages = mail.search(None, "ALL")
    mail.logout()
    if status != "OK":
        return []
    return messages[0].split()

# === Divide list into chunks for threading ===
def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# === Main Run ===
if __name__ == "__main__":
    email_ids = get_all_email_ids()
    if not email_ids:
        print("No emails found.")
        exit()

    chunks = list(chunk_list(email_ids, len(email_ids) // MAX_WORKERS + 1))
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(process_chunk, chunks)

    print("\n=== Summary ===")
    print(f"✅ Unsubscribed from: {unsubscribe_count}")
    print(f"🗑️ Emails deleted: {delete_count}")
