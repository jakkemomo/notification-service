from typing import List, Dict

import requests

from etl.settings import settings, logger


def get_emails_from_user_ids(recipients: List) -> Dict:
    """
    :param recipients: List of user ids.
    :return: Json data with user emails.
    """
    host = settings.auth_app.host
    port = settings.auth_app.port
    try:
        logger.info("Getting emails from Auth Service")
        recipients_data = {"ids": recipients}
        response = requests.get(f"http://{host}:{port}/emails", json=recipients_data)
        return response.json()
    except requests.exceptions.Timeout:
        logger.error("Timeout while connecting to Auth service!")
        return {}
    except requests.exceptions.TooManyRedirects:
        logger.error("Bad url for Auth service!")
        return {}
    except requests.exceptions.RequestException as e:
        logger.error("Something went wrong while connecting to Auth service!")
        return {}
