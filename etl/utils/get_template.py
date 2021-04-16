from typing import Dict

import requests

from etl.settings import settings, logger


def get_template_data(template_name: str) -> Dict:
    """
    :param template_name: Email template code name.
    :return: Json Data with string representation of html template.
    """
    host = settings.template_storage.host
    port = settings.template_storage.port
    final_response = {}
    logger.info("Getting emails from Template Storage Service")
    url = f"http://{host}:{port}/api/mail/template/{template_name}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            logger.error("Template Storage is not available, fix it!")
        else:
            final_response = response.json()
    except requests.exceptions.Timeout:
        logger.error("Timeout while connecting to Template Storage service!")
    except requests.exceptions.TooManyRedirects:
        logger.error("Bad url for Template Storage service!")
    except requests.exceptions.RequestException as e:
        logger.error("Something went wrong during Template Request: %s" % e)
    finally:
        return final_response
