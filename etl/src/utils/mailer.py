import email.utils
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from etl.src.settings import logger, settings

config = settings.mail_service
SENDER = config.sender
SENDERNAME = config.sender_name
USERNAME_SMTP = config.user
PASSWORD_SMTP = config.password
HOST = config.host
PORT = config.port


def send_email(recipient: str, subject: str, body_html: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = email.utils.formataddr((SENDERNAME, SENDER))
    msg["To"] = recipient
    html_part = MIMEText(body_html, "html")
    msg.attach(html_part)
    try:
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(SENDER, recipient, msg.as_string())
        server.close()
    except Exception as e:
        logger.error("Error: ", e)
    else:
        logger.info("Email sent!")
