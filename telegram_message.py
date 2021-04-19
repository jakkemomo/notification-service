import json
import logging
import os

import requests

logger = logging.getLogger(__name__)

steps_id_mapping = {
    "0": "actions/checkout@v2",
    "1": "Set up Python",
    "2": "Install dependencies",
    "3": "Refactor with pyupgrade",
    "4": "Refactor with isort",
    "5": "wemake-python-styleguide",
    "6": "Check types",
    "7": "Send result to telegram",
}
steps_string_json: str = os.getenv("STEPS_CONTEXT")
steps: dict = json.loads(steps_string_json)


def send_telegram():
    """
    This function send in our group chat message.
    :return: raise if not ok code
    """
    flow_result = "successfully"
    error = False
    step_with_error = ""
    project_name = os.getenv("GITHUB_REPOSITORY")
    commit_hash = os.getenv("GITHUB_SHA")
    for step in steps.keys():
        if not steps[step].get("success"):
            flow_result = "with error"
            error = True
            step_with_error = steps_id_mapping[step]
    message = f"{project_name}: Pipeline for {commit_hash} finished {flow_result}!"
    if error:
        message = f"{message}\n {step_with_error} failed!"

    token = os.getenv("BOT_TOKEN")
    url = "https://api.telegram.org/bot"
    channel_id = os.getenv("CHAT_ID")
    url += token
    method = "".join((url, "/sendMessage"))
    res = requests.post(
        method,
        data={
            "chat_id": channel_id,
            "text": message,
        },
    )

    if res.status_code != requests.codes.ok:
        raise ConnectionError("post_text error")


if __name__ == "__main__":
    # send_telegram()
    logger.info(steps)
