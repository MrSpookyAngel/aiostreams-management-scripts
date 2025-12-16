import json
import os
import time
import urllib.request
from utils import load_dotenv

# Usage: python refresh_all_users_addons.py
# This script updates all user accounts


def get_auth_key(email, password, login_url):
    """Fetches the auth key for the given email and password. Returns the auth key or None if there was an error."""

    USER_AGENT = os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
    )

    data = json.dumps(
        {
            "authKey": None,
            "email": email,
            "password": password,
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        login_url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
    )

    try:
        resp = urllib.request.urlopen(req, timeout=10)
        response = resp.read().decode("utf-8")
        response = json.loads(response)
        auth_key = response.get("result", {}).get("authKey", None)
        return auth_key
    except urllib.error.HTTPError:
        return None
    except urllib.error.URLError:
        print("Connection refused.")
        exit(1)


def get_addons(auth_key, base_url):
    """Fetches the addons for the given auth key. Returns a list of addons or None if there was an error."""

    USER_AGENT = os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
    )

    url = f"{base_url}/addonCollectionGet"
    data = json.dumps({"authKey": auth_key, "type": "AddonCollectionGet"}).encode(
        "utf-8"
    )

    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
    )

    try:
        resp = urllib.request.urlopen(req, timeout=10)
        response = resp.read().decode("utf-8")
        addons = json.loads(response).get("result", {}).get("addons", None)
        return addons
    except urllib.error.HTTPError:
        return None
    except urllib.error.URLError:
        print("Connection refused.")
        exit(1)


def update_addons(addons):
    """Updates the addon manifest to the latest version. Returns the updated addons."""

    USER_AGENT = os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
    )

    updated_addons = []

    for addon in addons:
        manifestUrl = addon.get("transportUrl", None)
        if manifestUrl is None:
            print(f"Manifest URL not found: {addon.get('id', 'unknown')}")
            exit(1)

        req = urllib.request.Request(
            manifestUrl,
            method="GET",
            headers={
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
            },
        )

        try:
            resp = urllib.request.urlopen(req, timeout=10)
            response = resp.read().decode("utf-8")
            manifest = json.loads(response)

            updated_addon = {
                **addon,
                "manifest": manifest,
            }

            if addon.get("manifest", {}).get("name") == "Cinemeta":
                catalogs = updated_addon.get("manifest", {}).get("catalogs", [])
                new_catalogs = [
                    c
                    for c in catalogs
                    if c.get("id") in ["last-videos", "calendar-videos"]
                ]
                updated_addon["manifest"]["catalogs"] = new_catalogs
                updated_addon["manifest"]["resources"] = ["catalog", "addon_catalog"]

            updated_addons.append(updated_addon)
        except urllib.error.HTTPError:
            continue
        except urllib.error.URLError:
            print(f"Connection refused. Keeping original addon manifest: {manifestUrl}")
            updated_addons.append(addon)
            continue

    return updated_addons if updated_addons else None


def set_addons(auth_key, addons, base_url):
    """Sets the addons for the given auth key. Returns the response from the server or None if there was an error."""

    USER_AGENT = os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
    )

    url = f"{base_url}/addonCollectionSet"
    data = json.dumps(
        {
            "authKey": auth_key,
            "type": "AddonCollectionSet",
            "addons": addons,
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
    )

    try:
        resp = urllib.request.urlopen(req, timeout=10)
        response = resp.read().decode("utf-8")
        success = json.loads(response).get("result", {}).get("success", False)
        return success
    except urllib.error.HTTPError:
        return False
    except urllib.error.URLError:
        print("Connection refused.")
        exit(1)


def main():
    load_dotenv()

    BASE_STREMIO_API_URL = os.getenv("BASE_STREMIO_API_URL")
    STREMIO_ACCOUNTS_JSON_PATH = os.getenv("STREMIO_ACCOUNTS_JSON_PATH")

    if not all([BASE_STREMIO_API_URL, STREMIO_ACCOUNTS_JSON_PATH]):
        print("One or more environment variables are not set.")
        return

    if BASE_STREMIO_API_URL.endswith("/"):
        BASE_STREMIO_API_URL = BASE_STREMIO_API_URL[:-1]

    LOGIN_URL = f"{BASE_STREMIO_API_URL}/login"

    with open(STREMIO_ACCOUNTS_JSON_PATH, "r", encoding="utf-8") as f:
        accounts = json.load(f)["accounts"]

    for account in accounts:
        email = account["email"]
        password = account["password"]

        print(f"Processing account: {email}")

        auth_key = get_auth_key(email, password, LOGIN_URL)
        if auth_key is None:
            print(f"Failed to retrieve auth key: {email}")
            exit(1)

        addons = get_addons(auth_key, BASE_STREMIO_API_URL)
        if addons is None:
            print(f"Failed to retrieve addons: {email}")
            exit(1)

        updated_addons = update_addons(addons)
        if updated_addons is None:
            print(f"Failed to update addons: {email}")
            exit(1)

        success = set_addons(auth_key, updated_addons, BASE_STREMIO_API_URL)
        if not success:
            print(f"Failed to update addons: {email}")
            exit(1)

        print(f"Successfully updated addons: {email}")

        time.sleep(1)


if __name__ == "__main__":
    main()
