import os
import smtplib
from email.message import EmailMessage


def send_outreach_email(to_email, subject, body):
    sender_email = os.getenv("SCOUTAI_EMAIL")
    sender_password = os.getenv("SCOUTAI_EMAIL_PASSWORD")

    if not sender_email or not sender_password:
        return {
            "success": False,
            "message": "Email credentials are missing. Set SCOUTAI_EMAIL and SCOUTAI_EMAIL_PASSWORD."
        }

    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(message)

        return {
            "success": True,
            "message": f"Email sent successfully to {to_email}"
        }

    except Exception as error:
        return {
            "success": False,
            "message": str(error)
        }