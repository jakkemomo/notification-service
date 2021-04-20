from etl.src.celery_app import app
from etl.src.models import EmailMessage, MessageIn, WebsocketMessage
from etl.src.settings import logger
from etl.src.utils.email_queue import (
    enrich_message_with_template_data,
    get_email_addresses_from_ids,
    get_template_data_by_name,
    send_email_messages,
)
from etl.src.utils.websocket import send_websocket_messages


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
                **message.dict(),
                subject=template_data.get("subject"),
                body_html=template_data.get("body"),
            )
            enrich_message_with_template_data(email_message)
            send_email_messages(email_message)
        else:
            logger.error("Couldn't find any templates with given name!")
    else:
        logger.error("Couldn't find any emails!")


@app.task(name="websocket.process_websocket_query")
def process_websocket_query(payload: dict) -> None:
    """
    Process Websocket Queue.
    :return: None.
    """
    logger.info("Processing Websocket")
    logger.info(payload)
    message = MessageIn(**payload)
    template = get_template_data_by_name(message)
    if not template:
        logger.error("Couldn't find any templates with given name!")
        return

    ws_msg = WebsocketMessage(
        **message.dict(),
        body_html=template.get("body"),
    )
    enrich_message_with_template_data(ws_msg)
    send_websocket_messages(ws_msg)
