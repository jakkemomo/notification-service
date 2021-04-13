import email.utils
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from etl.settings import settings, logger

config = settings.mail_service
SENDER = config.sender
SENDERNAME = config.sender_name
USERNAME_SMTP = config.user
PASSWORD_SMTP = config.password
HOST = config.host
PORT = config.port


def send_mail(recipients: List, subject: str, body_text: str, body_html: str) -> None:
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = email.utils.formataddr((SENDERNAME, SENDER))
    msg["To"] = ", ".join(recipients)
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(body_text, "plain")
    part2 = MIMEText(body_html, "html")
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    # Try to send the message.
    try:
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        # stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(SENDER, recipients, msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        logger.error("Error: ", e)
    else:
        logger.info("Email sent!")


if __name__ == "__main__":
    RECIPIENT = "alexolikov@gmail.com"
    # The subject line of the email.
    SUBJECT = "Amazon SES Test (Python smtplib)"
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = (
        "Amazon SES Test\r\n"
        "This email was sent through the Amazon SES SMTP "
        "Interface using the Python smtplib package."
    )
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Amazon SES SMTP Email Test</h1>
    <p>This email was sent with Amazon SES using the
    <a href='https://www.python.org/'>Python</a>
    <a href='https://docs.python.org/3/library/smtplib.html'>
    smtplib</a> library.</p>
    </body>
    </html>
            """

    send_mail([RECIPIENT], SUBJECT, BODY_TEXT, BODY_HTML)
