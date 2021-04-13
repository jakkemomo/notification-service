from typing import List, Dict

import requests

from etl.settings import settings, logger


def get_emails_from_user_ids(recipients: List) -> Dict:
    host = settings.auth_app.host
    port = settings.auth_app.port
    try:
        logger.info("Getting emails from Auth Service")
        data = {"ids": recipients}
        response = requests.get(f"http://{host}:{port}/emails", json=data)
        return response.json()
    except requests.exceptions.Timeout:
        logger.error("Timeout while connecting to Auth service!")
    except requests.exceptions.TooManyRedirects:
        logger.error("Bad url for Auth service!")
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
