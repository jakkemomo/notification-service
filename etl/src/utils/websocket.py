import logging
from time import sleep

import requests

from etl.src.models import WebsocketMessage
from etl.src.settings import settings

logger = logging.getLogger(__name__)


def send_websocket_message(user_id: str, message: str):
    """
    Sending websocket message to Websocket Service.
    :param user_id: string with user identifier
    :param message: string with filled body_html and recipients.
    :return: None.
    """
    scheme = settings.websocket.scheme
    host = settings.websocket.host
    port = settings.websocket.port

    url = f"{scheme}://{host}:{port}/notifications/{user_id}"
    data = {"message": message}

    logger.info("Websocket message sending...")
    try:
        response = requests.post(url, json=data)
        if response.status_code != 200:
            logger.error(
                "Websocket returned status code [%s]. Response: [%s]" %
                (response.status_code, response.json())
            )
    except requests.exceptions.RequestException as e:
        logger.error("Error while request sending to Websocket service : %s" % e)


def send_websocket_messages(message: WebsocketMessage, sleep_time: int = 0) -> None:
    """
    Main method for sending websocket message to Websocket Service.
    :param message: WebsocketMessage object with filled body_html.
    :param sleep_time: optional time for delay.
    :return: None.
    """
    for recipient in message.recipients:
        send_websocket_message(recipient, message.body_html)
        sleep(sleep_time)
