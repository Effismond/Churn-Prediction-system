import smtplib
from email.message import EmailMessage
import os


def send_alert(subject: str, body: str, to_email: str):
    EMAIL_ADDRESS = os.getenv("ALERT_EMAIL")
    EMAIL_PASSWORD = os.getenv("ALERT_EMAIL_PASSWORD")

    # 👇 SAFE EXIT (very important for Streamlit/Render)
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("⚠️ Email credentials not set. Skipping alert.")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("✅ Alert sent successfully")
