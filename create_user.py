import os
import json
import secrets
import urllib.request
import urllib.parse
from utils import load_dotenv

# Usage: python create_user.py
# This script creates a new user account with a random password.


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

    with open(AIOSTREAMS_CONFIG_PATH, "r", encoding="utf-8") as f:
        aiostreams_config = json.load(f)

    password = secrets.token_urlsafe(128)

    data = json.dumps(
        {
            "config": aiostreams_config,
            "password": password,
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=data,
        method="PUT",
        headers={"Content-Type": "application/json"},
    )

    try:
        resp = urllib.request.urlopen(req, timeout=10)
        response = resp.read().decode("utf-8")
        response = json.loads(response)

        if not response.get("success"):
            print(f"Failed to create user: {response.get('error')}")
            return
    except urllib.error.HTTPError as e:
        print(f"Failed to create user: {e}")
        return

    uuid = response.get("data", {}).get("uuid")
    encrypted_password = response.get("data", {}).get("encryptedPassword")
    manifest_url = f"{BASE_URL}/stremio/{uuid}/{encrypted_password}/manifest.json"
    encoded_manifest_url = urllib.parse.quote(manifest_url, safe=":/")
    account = {"uuid": uuid, "password": password, "manifest": encoded_manifest_url}
    print(f"User created successfully: {account}")

    with open(ACCOUNTS_JSON_PATH, "r+", encoding="utf-8") as f:
        data = json.load(f)
        data["accounts"].append(account)
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()


if __name__ == "__main__":
    main()
