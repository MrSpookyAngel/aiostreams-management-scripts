import json
import os
import time
import urllib.request
from utils import load_dotenv

# Usage: python update_all_users.py
# This script updates all user accounts with the latest configuration.


def main():
    load_dotenv()

    BASE_URL = os.getenv("BASE_URL")
    ACCOUNTS_JSON_PATH = os.getenv("ACCOUNTS_JSON_PATH")
    AIOSTREAMS_CONFIG_PATH = os.getenv("AIOSTREAMS_CONFIG_PATH")

    if not all([BASE_URL, ACCOUNTS_JSON_PATH, AIOSTREAMS_CONFIG_PATH]):
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
        password = account["password"]

        print(f"Processing account: {uuid}")

        data = json.dumps(
            {
                "uuid": uuid,
                "password": password,
                "config": aiostreams_config,
            }
        ).encode("utf-8")

        req = urllib.request.Request(
            API_URL,
            data=data,
            method="POST",
            headers={"Content-Type": "application/json"},
        )

        try:
            resp = urllib.request.urlopen(req, timeout=10)
            response = resp.read().decode("utf-8")
            response = json.loads(response)

            if not response.get("success"):
                print(f"Failed to process account: {response.get('error')}")
                continue
        except urllib.error.HTTPError:
            print(f"Failed to process account: {uuid}")
            continue

        print(f"Successfully processed account: {uuid}")

        time.sleep(1)


if __name__ == "__main__":
    main()
