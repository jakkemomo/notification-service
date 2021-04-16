from time import sleep
from typing import Dict, List

from etl.celery_app import app
from etl.mailer import send_mail
from etl.models import MessageIn, EmailMessage
from etl.settings import logger
from etl.utils.get_emails import get_emails_from_user_ids
from etl.utils.get_template import get_template_data
from etl.utils.html_to_text import HTMLFilter
from template_mailer import render_template


def get_email_addresses_from_ids(recipients: List) -> List:
    """
    :param recipients: List of user ids.
    :return: List of user emails.
    """
    email_data: Dict = get_emails_from_user_ids(recipients)
    emails: List = email_data.get("emails", [])
    return emails


def get_template_data_by_name(message: MessageIn) -> dict:
    """
    :param message: MessageIn object with values from Notify API.
    :return: MessageIn object with template data loaded from Django App.
    """
    template_name = message.template_name
    template_data = get_template_data(template_name)
    return template_data


def enrich_email_with_template_vals(email_message: EmailMessage):
    """
    :param email_message: Message object.
    :return: Message object with enriched values in template variable.
    """
    template_data = email_message.template_data
    template: str = email_message.body_html

    email_message.body_html = render_template(template, template_data)
    email_message.body_text = HTMLFilter.convert_html_to_text(email_message.body_html)

    return email_message


def send_email_message(message: EmailMessage, sleep_time: int = 0) -> None:
    """
    Main method for sending email message through Amazon SES.
    :param message: MessageIn object with filled body_html, body_text, subject and recipients.
    :param sleep_time: optional time for delay.
    :return: None.
    """
    sleep(sleep_time)
    for recipient in message.recipients:
        send_mail(
            recipient=recipient,
            subject=message.subject,
            body_html=message.body_html,
            body_text=message.body_text,
        )


@app.task(name="email.process_email_query")
def process_email_query(payload: dict) -> None:
    """
    Process Email Queue: send messages to Amazon SES.
    :param payload: dictionary with data from Notify API.
    :return: None.
    """
    logger.info("Processing Emails")
    message = MessageIn(**payload)
    emails = get_email_addresses_from_ids(message.recipients)
    if emails:
        message.recipients = emails
        logger.info(f"Got emails from Auth Service: {emails}")
        template_data = get_template_data_by_name(message)
        if template_data:
            email_message = EmailMessage(
                recipients=emails,
                template_data=message.template_data,
                subject=template_data.get("subject"),
                body_html=template_data.get("body"),
            )
            enrich_email_with_template_vals(email_message)
            # send_email_message(email_message)
        else:
            logger.error("Couldn't find any templates with given name!")
    else:
        logger.error("Couldn't find any emails!")


@app.task(name="websocket.process_websocket_query")
def process_websocket_query(payload: dict) -> None:
    print("Processing Websocket")


in_message = MessageIn(**{
    "recipients": [
        "238775e8-0e56-4bf8-b220-47bf3a23593e", "3622887c-084b-422f-8fd3-02cd72ae66d3"
    ],
    "template_name": "user_registration",
    "template_data": {"name": "Loshok-Petyshok"}
})
get_template_data_by_name(in_message)
