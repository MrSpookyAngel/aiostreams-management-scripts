# AIOStreams Management Scripts (unofficial)

## Reasoning Behind This

I got annoyed of juggling account configurations for my family, so I decided to make some scripts to do it for me!

# Create User

## Purpose

Creates a new user account with a random password using the config at `AIOSTREAMS_CONFIG_PATH` and adds it to the accounts.json at `ACCOUNTS_JSON_PATH`

## Command

```
python create_user.py
```

## Example Usage

```
python create_user.py
User created successfully: {'uuid': 'ce4ce4cd-f733-4dae-be68-601e92eb02da', 'password': 'GRAcmTLjGD38HTJJM32zjdTkUFIH15uw5g3PciflSmgmKULVynsEoWn4cUdS0kI-uqK67pTilbjt0mm0jpS98oRwACo2XyI27yuxOKcACwBqlDUHt_Wb1jFQhygs8n_Adz1zCZlaMOccMcxH6LBuOSzxGMzbCOULu19CT7PH71U', 'manifest': 'https://<your-domain>/stremio/ce4ce4cd-f733-4dae-be68-601e92eb02da/eyJpdiI6ImVPN0pFaWpKRlJCMmduZDh2OFdCNVE9PSIsImVuY3J5cHRlZCI6ImVVNGkyQVJvY1pjRWgvU3ZyR3VLazlsWTByZTF5UU0vRDlTRStFRXQxTFVoRnRPdXZINjY2WUlhWFF1am9sT2QwSGxGRlVDcjZyejN3Y3VoRnAzUW9Md2V4dWttM0hJTmZuekF2Wit3V0JvWUJDdndqQ0ZGaEJ5cGxVQ1J5d21TWnZQZHJGc2dGcVNubTFDNFU4RVNHejFOMjV3dllxWDk3K0FVOVhwTHZwazJFZUtmOFliODlTOXo2MXREdCtlV3lxMWlwLzF6SHg3ekswcEdQQWZXeXk0ZU14SVA0UFkrdkV5QXdvaG5seDQ9IiwidHlwZSI6ImFpb0VuY3J5cHQifQ/manifest.json'}
```

# Delete User

## Purpose

Deletes a user account using the password located in the accounts.json at `ACCOUNTS_JSON_PATH` and also removes it from there

## Command

```
python delete_user.py
```

## Example Usage

```
Enter the UUID of the user to delete: ce4ce4cd-f733-4dae-be68-601e92eb02da
Processing account: ce4ce4cd-f733-4dae-be68-601e92eb02da
Successfully deleted user: ce4ce4cd-f733-4dae-be68-601e92eb02da
```

# Update All Users

## Purpose

Updates all user accounts located in the accounts.json at `ACCOUNTS_JSON_PATH` with the configuration at `AIOSTREAMS_CONFIG_PATH`

## Command

```
python update_all_users.py
```

## Example Usage

```
python update_all_users.py
Processing account: ce4ce4cd-f733-4dae-be68-601e92eb02da
Successfully updated account: ce4ce4cd-f733-4dae-be68-601e92eb02da
```

# Refresh All Users Addons (Experimental)

## Purpose

It updates the addons for all the users located in the stremio_accounts.json at `STREMIO_ACCOUNTS_JSON_PATH`. NOTE: It comes with the added benefit of removing parts of Cinemeta for better compatibility with [AIOMetadata](https://github.com/cedya77/aiometadata). Inspired from [Cinebye](https://github.com/0xConstant1/stremio-addon-manager).

## Example Usage

```
python refresh_all_users_addons.py
Processing account: email1@example.com
Successfully updated addons: email1@example.com
```

## Note

- From experimenting, it sometimes throws a connection refused error. Just try again later.
- If it fails anywhere, the program should exit, but there's no guarantee your configuration won't break. If something does break, then running [this](https://web.archive.org/web/20250220150116id_/https://pastebin.com/raw/VUPfMnGk) in your browser console on [Stremio Web](https://web.stremio.com) should completely reset your Stremio account addons as if you just created a new account.
