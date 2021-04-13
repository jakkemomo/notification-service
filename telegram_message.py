import json
import os

import requests

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
    result = "successfully"
    error = False
    step = ""
    project_name = os.getenv("GITHUB_REPOSITORY")
    commit_hash = os.getenv("GITHUB_SHA")
    for step in steps:
        if not steps[step].get("success"):
            result = "with error"
            error = True
            step = steps_id_mapping[step]
    message = f"{project_name}: Pipeline for {commit_hash} finished {result}!"
    if error:
        message += f"\n {step} failed!"

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
    print(os.environ)
