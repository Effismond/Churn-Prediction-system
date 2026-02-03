import smtplib
from email.message import EmailMessage
import os


def send_alert(subject: str, body: str, to_email: str):
    """
    Send email alert when an issue (e.g. data drift) is detected.
    """

    EMAIL_ADDRESS = os.getenv("ALERT_EMAIL")
    EMAIL_PASSWORD = os.getenv("ALERT_EMAIL_PASSWORD")

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise ValueError("Email credentials not set in environment variables")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("✅ Alert sent successfully")