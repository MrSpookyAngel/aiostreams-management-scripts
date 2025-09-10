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
User created successfully: {'uuid': '7b4d00ac-aa20-4e44-ad19-8e8f2ed23f71', 'password': '0ousjsMIZDRY4Sobi67PWoSY2g5fzdLO5MpXrBSN6i9m4FmzPBalWt2lV3uJWAG3rQDTBzRRMtj1TDYMTnF4YO9Lwe10YzIY-6CeiX6F_tWwAwzIH7lsnXgVB5goNLGmpGleF5GGHrCMczM_BADgP11auVUhVOWmnjsE17zH1yY'}
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
Enter the UUID of the user to delete: 7b4d00ac-aa20-4e44-ad19-8e8f2ed23f71
Processing account: 7b4d00ac-aa20-4e44-ad19-8e8f2ed23f71
Successfully deleted user: 7b4d00ac-aa20-4e44-ad19-8e8f2ed23f71
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
Processing account: 7b4d00ac-aa20-4e44-ad19-8e8f2ed23f71
Successfully processed account: 7b4d00ac-aa20-4e44-ad19-8e8f2ed23f71
```
