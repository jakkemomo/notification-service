from time import sleep
from typing import Dict, List

from etl.celery_app import app
from etl.mailer import send_mail
from etl.models import MessageIn
from etl.utils.get_emails import get_emails_from_user_ids
from etl.utils.get_template import get_template_data
from etl.utils.html_to_text import HTMLFilter


@app.task
def enrich_email_with_email_addresses(recipients: List) -> List:
    """
    :param recipients: List of user ids.
    :return: List of user emails.
    """
    email_data: Dict = get_emails_from_user_ids(recipients)
    emails: List = email_data.get("emails", [])
    return emails


@app.task
def get_template_by_name(message_data: dict) -> MessageIn:
    """
    :param message_data: Dictionary with values from Notify API.
    :return: MessageIn object with template data loaded from Django App.
    """
    template_name = message_data.get("template_name")
    # go to django app to get template
    template_data = get_template_data(template_name)
    # return a MessageIn object
    message = MessageIn(
        template_name=template_data.get("name"),
        subject=template_data.get("subject"),
        body_html=template_data.get("body"),
        recipients=message_data.get("recipients", []),
        template_data=message_data.get("template_data", {}),
    )
    return message


@app.task
def enrich_email_with_template_vals(message: MessageIn):
    """
    :param message: Message object.
    :return: Message object with enriched values in template variable.
    """
    # grab template data and try to enter it in template
    template_data = message.template_data
    template: str = message.body_html

    # Swap Binary substring
    # Using translate()
    for variable_key, variable_value in template_data.items():
        # todo: rework maketrans
        temp = str.maketrans(f"{{ {variable_key} }}", str(variable_value))
        template = template.translate(temp)
    message.body_html = template
    body_text: str = HTMLFilter.convert_html_to_text(template)
    message.body_text = body_text
    return message


@app.task
def send_email_message(message: MessageIn, sleep_time: int = 0) -> None:
    """
    Main method for sending email message through Amazon SES.
    :param message: MessageIn object with filled body_html, body_text, subject and recipients.
    :param sleep_time: optional time for delay.
    :return: None.
    """
    sleep(sleep_time)
    send_mail(
        recipients=message.recipients,
        subject=message.subject,
        body_html=message.body_html,
        body_text=message.body_text,
    )


# enrich_email_with_email_addresses(
#     recipients=[
#         "238775e8-0e56-4bf8-b220-47bf3a23593e",
#         "3622887c-084b-422f-8fd3-02cd72ae66d3",
#     ]
# )
get_template_by_name({"template_name": "user_registration"})
