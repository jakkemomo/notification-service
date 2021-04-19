from time import sleep
from typing import Dict, List


from etl.models import MessageIn, EmailMessage
from etl.settings import logger
from etl.utils.get_emails import get_emails_from_user_ids
from etl.utils.get_template import get_template_data
from template_mailer import render_template

from etl.utils.mailer import send_email


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
    try:
        template_data = get_template_data(template_name)
        return template_data
    except Exception as e:
        logger.error(f"Error while enriching message with values: {e}")
        return {}


def enrich_message_with_template_data(email_message: EmailMessage):
    """
    :param email_message: Message object.
    :return: Message object with enriched values in template variable.
    """
    template_data = email_message.template_data
    template: str = email_message.body_html

    email_message.body_html = render_template(template, template_data)

    return email_message


def send_email_messages(message: EmailMessage, sleep_time: int = 0) -> None:
    """
    Main method for sending email message through Amazon SES.
    :param message: MessageIn object with filled body_html, subject and recipients.
    :param sleep_time: optional time for delay.
    :return: None.
    """
    sleep(sleep_time)
    # todo: abstract
    for recipient in message.recipients:
        send_email(
            recipient=recipient,
            subject=message.subject,
            body_html=message.body_html,
        )