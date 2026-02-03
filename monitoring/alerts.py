import smtplib
from email.message import EmailMessage

def send_alert(subject, body, to_email):
    """
    Send email alert
    """
    # configure your email settings
    EMAIL_ADDRESS = "your_email@example.com"
    EMAIL_PASSWORD = "your_app_password"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("✅ Alert sent successfully")
    
# Example usage:
# send_alert("Data Drift Alert", "Data drift detected in Churn pipeline", "recipient@example.com")