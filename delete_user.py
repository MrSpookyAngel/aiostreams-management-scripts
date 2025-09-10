import os
import json
import urllib.request
from utils import load_dotenv

# Usage: python delete_user.py
# This script deletes a user account.
# Input: <UUID>


def main():
    load_dotenv()

    BASE_URL = os.getenv("BASE_URL")
    ACCOUNTS_JSON_PATH = os.getenv("ACCOUNTS_JSON_PATH")

    if not all([BASE_URL, ACCOUNTS_JSON_PATH]):
        print("One or more environment variables are not set.")
        return

    if BASE_URL.endswith("/"):
        BASE_URL = BASE_URL[:-1]

    API_URL = f"{BASE_URL}/api/v1/user"

    uuid_to_delete = input("Enter the UUID of the user to delete: ").strip()
    password = None

    with open(ACCOUNTS_JSON_PATH, "r", encoding="utf-8") as f:
        accounts = json.load(f).get("accounts", [])

    for account in accounts:
        uuid = account["uuid"]
        if uuid == uuid_to_delete:
            password = account["password"]
            break
    if password is None:
        print(f"Account not found: {uuid_to_delete}")
        return

    print(f"Processing account: {uuid}")

    data = json.dumps(
        {
            "uuid": uuid,
            "password": password,
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=data,
        method="DELETE",
        headers={"Content-Type": "application/json"},
    )

    try:
        resp = urllib.request.urlopen(req, timeout=10)
        response = resp.read().decode("utf-8")
        response = json.loads(response)

        if not response.get("success"):
            print(f"Failed to delete user: {response.get('error')}")
            return
    except urllib.error.HTTPError:
        print(f"Failed to process account: {uuid}")
        return

    print(f"Successfully deleted user: {uuid}")

    with open(ACCOUNTS_JSON_PATH, "r+", encoding="utf-8") as f:
        data = json.load(f)
        data["accounts"] = [acc for acc in data["accounts"] if acc["uuid"] != uuid]
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.truncate()


if __name__ == "__main__":
    main()
