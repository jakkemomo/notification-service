from typing import Dict

import requests

from etl.settings import settings, logger


def get_template(template_name: str) -> Dict:
    """
    :param template_name: Email template code name
    :return: Json Data with string representation of html template
    """
    host = settings.template_storage.host
    port = settings.template_storage.port
    try:
        logger.info("Getting emails from Template Storage Service")
        response = requests.get(f"http://{host}:{port}/template/{template_name}")
        return response.json()
    except requests.exceptions.Timeout:
        logger.error("Timeout while connecting to Template Storage service!")
        return {}
    except requests.exceptions.TooManyRedirects:
        logger.error("Bad url for Template Storage service!")
        return {}
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
