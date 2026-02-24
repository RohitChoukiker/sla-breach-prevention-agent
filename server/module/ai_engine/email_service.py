import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time


def send_escalation_email(state):

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    escalation_receiver = os.getenv("ESCALATION_EMAIL")

    subject = f"SLA Escalation Alert - Ticket {state['ticket_id']}"

    body = f"""
    SLA Breach Alert

    Ticket ID: {state['ticket_id']}
    Probability: {state['breach_probability']}
    Confidence: {state['confidence_score']}
    Priority: {state['priority']}

    Immediate attention required.
    """

    message = MIMEMultipart()
    message["From"] = smtp_user
    message["To"] = escalation_receiver
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    max_retries = 3

    for attempt in range(max_retries):
        try:
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(
                smtp_user,
                escalation_receiver,
                message.as_string()
            )
            server.quit()

            print(f"Escalation email sent for {state['ticket_id']}")
            return

        except Exception as e:
            print(f"Email send failed (attempt {attempt+1}): {e}")
            time.sleep(2)

    print("Email permanently failed after retries")
