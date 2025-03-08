import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import datetime

# Load env variables
load_dotenv()
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
db_name = os.getenv("MONGO_DB_NAME")
cluster = os.getenv("MONGO_CLUSTER")

uri = f"mongodb+srv://{username}:{password}@{cluster}/{db_name}?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client[db_name]
complaints_collection = db['complaints']


#email
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")

def process_complaint(state, lga, street, complaint_text, chairman_email):
    subject = f"New Complaint from {street}, {lga} LGA, {state} State"

    body = f"""
Dear Chairman,

A new complaint has been submitted from a resident of {street} in {lga} LGA, {state} State.

The complaint is as follows:

"{complaint_text}"

This message was sent via the PSNG platform.

Regards,
PSNG System
"""

    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = chairman_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)

        print(f"✅ Complaint email sent to {chairman_email}")

        complaint_doc = {
            "state": state,
            "lga": lga,
            "street": street,
            "complaint": complaint_text,
            "sent_to": chairman_email,
            "submitted_at": datetime.datetime.utcnow()
        }
        complaints_collection.insert_one(complaint_doc)
        print("✅ Complaint saved to MongoDB.")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        print("⚠️ Complaint not saved to MongoDB.")
