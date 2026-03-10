import smtplib
import os
import logging

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)


def send_escalation_email(state):

    try:

        print("[Email] Preparing escalation email")

        ticket_id = state["ticket_id"]
        probability = state["breach_probability"]
        priority = state["priority"]

        sender = os.getenv("EMAIL_USER")
        receiver = os.getenv("ESCALATION_EMAIL")
        password = os.getenv("EMAIL_PASSWORD")

        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))

        subject = f"SLA Breach Risk Alert - Ticket {ticket_id}"

        body = f"""
Hello,

An SLA breach risk has been detected.

Ticket ID: {ticket_id}
Priority: {priority}
Breach Probability: {round(probability * 100, 2)}%

Immediate attention is required.

Regards,
SLA Prevention System
"""

        msg = MIMEMultipart()

        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        print("[Email] Connecting SMTP server...")

        server = smtplib.SMTP(smtp_server, smtp_port)

        server.starttls()

        server.login(sender, password)

        server.sendmail(
            sender,
            receiver,
            msg.as_string()
        )

        server.quit()

        print("[Email] Escalation email sent")

        logger.info(f"Escalation email sent for ticket {ticket_id}")

    except Exception as e:

        print("[Email ERROR]", str(e))

        logger.error(f"Email sending failed: {str(e)}")