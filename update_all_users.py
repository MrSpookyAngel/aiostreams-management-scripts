import base64
import json
import os
import time
import urllib.request

from utils import load_dotenv


def main():
    load_dotenv()

    BASE_URL = os.getenv("BASE_URL")
    ACCOUNTS_JSON_PATH = os.getenv("ACCOUNTS_JSON_PATH")
    AIOSTREAMS_CONFIG_PATH = os.getenv("AIOSTREAMS_CONFIG_PATH")
    CONFIG_ACCESS_KEY = os.getenv("CONFIG_ACCESS_KEY")

    USER_AGENT = os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
    )

    if not all(
        [BASE_URL, ACCOUNTS_JSON_PATH, AIOSTREAMS_CONFIG_PATH, CONFIG_ACCESS_KEY]
    ):
        print("One or more environment variables are not set.")
        return

    if BASE_URL.endswith("/"):
        BASE_URL = BASE_URL[:-1]

    API_URL = f"{BASE_URL}/api/v1/user"

    with open(ACCOUNTS_JSON_PATH, "r", encoding="utf-8") as f:
        accounts = json.load(f)["accounts"]

    with open(AIOSTREAMS_CONFIG_PATH, "r", encoding="utf-8") as f:
        aiostreams_config = json.load(f)

    for account in accounts:
        uuid = account["uuid"]

        print(f"Processing account: {uuid}")

        password = account["password"]

        credentials = f"{uuid}:{password}"
        base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode(
            "utf-8"
        )

        data = json.dumps(
            {
                "config": {
                    **aiostreams_config,
                    "accessKey": CONFIG_ACCESS_KEY,
                }
            }
        ).encode("utf-8")

        req = urllib.request.Request(
            API_URL,
            data=data,
            method="PUT",
            headers={
                "Authorization": f"Basic {base64_credentials}",
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
            },
        )

        try:
            resp = urllib.request.urlopen(req, timeout=10)
            response = json.loads(resp.read().decode("utf-8"))
            if not response.get("success"):
                print(f"Failed to update account {uuid}: {response.get('error')}")
                continue
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8")
            print(f"Failed to update account {uuid}: HTTP {e.code} - {body}")
            continue

        print(f"Successfully updated account: {uuid}")

        time.sleep(1)


if __name__ == "__main__":
    main()
