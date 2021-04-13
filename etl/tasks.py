from time import sleep
from typing import Dict, List

from etl.celery_app import app
from etl.mailer import send_mail
from etl.models import EmailMessage
from etl.utils.get_emails import get_emails_from_user_ids
from etl.utils.get_template import get_template
from etl.utils.html_to_text import HTMLFilter


@app.task
def enrich_email_with_email_addresses(recipients: List) -> List:
    # go to auth service and grab emails
    # recipients = message.recipients
    data: Dict = get_emails_from_user_ids(recipients)

    # add emails to message data
    # message.recipients = list(emails.values())
    emails: List = data.get("emails", [])
    print(emails)
    return emails


@app.task
def get_template_by_name(data: dict) -> EmailMessage:
    template_name = data.get("template_name")
    # go to django app to get template
    template = get_template(template_name)
    # return a EmailMessage object
    message = EmailMessage(
        template=template,
        template_name=template_name,
        recipients=data.get("recipients", []),
        subject=data.get("subject", ""),
    )
    return message


@app.task
def enrich_email_with_template_vals(message: EmailMessage):
    # grab template data and try to enter it in template
    data = message.template_data
    template = message.template

    # Swap Binary substring
    # Using translate()
    for key, value in data.items():
        temp = str.maketrans(f"{{ {key} }}", str(value))
        template = template.translate(temp)
    message.body_html = template
    body_text = HTMLFilter.convert_html_to_text(template)
    message.body_text = body_text
    return message


@app.task
def send_email_message(message: EmailMessage, sleep_time: int):
    sleep(sleep_time)
    send_mail(
        recipients=message.recipients,
        subject=message.subject,
        body_html=message.body_html,
        body_text=message.body_text,
    )


enrich_email_with_email_addresses(
    recipients=[
        "238775e8-0e56-4bf8-b220-47bf3a23593e",
        "3622887c-084b-422f-8fd3-02cd72ae66d3",
    ]
)
