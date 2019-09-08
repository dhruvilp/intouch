import json

class PATHS:
    NEW_USER = "/new_user"
    NEW_CONNECTION = "/new_connection"
    EDIT_CONNECTION = "/edit_connection"
    GET_CONNECTION = "/get_connection"
    GET_CONNECTIONS = "/get_connections"

PROJECT_ID = "intouch-6a524"

with open("secrets.json", "r") as read_file:
    data = json.load(read_file)
    ACCOUNT_SID = data["account_sid"]
    AUTH_TOKEN = data["auth_token"]