import requests
from exceptions import ClientRequestException, InvalidEnvException
import common
import logging
import json

logging.getLogger().setLevel(logging.INFO)


class InTouchClient:

    def __init__(self, env=None):
        env = env or "DEV"
        if env not in ["DEV", "PROD"]:
            raise InvalidEnvException()
        if env == "DEV":
            logging.info("[InTouchClient] started client in DEV environment")
            self.url = "http://localhost:8080{}"
        if env == "PROD":
            logging.info("[InTouchClient] started client in PROD environment")
            self.url = "http://{}.appspot.com".format(common.PROJECT_ID) + "{}"

    def post(self, path, data):
        request_url = self.url.format(path)
        resp = requests.post(request_url, json=data)
        logging.info("[post] made post request to url %s", request_url)
        if resp.status_code != 200:
            raise ClientRequestException("HTTP {}: {}".format(resp.status_code, resp.reason))
        return resp

    def new_user(self, id, auth_code, phone_number, name):
        logging.info(
            "[new_user] id=%s, auth_code=%s, phone_number=%s, name=%s" % (id, auth_code, phone_number, name))
        data = {'id': id,
                'auth_code': auth_code,
                'phone_number': phone_number,
                'name': name}
        self.post(common.PATHS.NEW_USER, data)

    def new_connection(self, id, connection_name, frequency, how_you_met, their_challenges, other_notes):
        logging.info(
            '[new_connection] id=%s, connection_name=%s, frequency=%s, how_you_met=%s, their_challenges=%s, other_notes=%s' % (
                id, connection_name, frequency, how_you_met, their_challenges, other_notes))
        data = {'id': id,
                'connection_name': connection_name,
                'frequency': frequency,
                'how_you_met': how_you_met,
                'their_challenges': their_challenges,
                'other_notes': other_notes}
        self.post(common.PATHS.NEW_CONNECTION, data)

    def update_connection(self, id, connection_name, frequency=None, how_you_met=None, their_challenges=None,
                          other_notes=None):
        logging.info(
            '[new_connection] id=%s, connection_name=%s, frequency=%s, how_you_met=%s, their_challenges=%s, other_notes=%s' % (
                id, connection_name, frequency, how_you_met, their_challenges, other_notes))
        data = {'id': id,
                'connection_name': connection_name,
                'frequency': frequency,
                'how_you_met': how_you_met,
                'their_challenges': their_challenges,
                'other_notes': other_notes}
        data = {k: v for k, v in data.items() if v is not None}
        self.post(common.PATHS.EDIT_CONNECTION, data)

    def get_connection(self, id, connection_name):
        logging.info("[get_connection] id=%s, connection_name=%s", id, connection_name)
        data = {"id": id,
                "connection_name": connection_name}
        resp = self.post(common.PATHS.GET_CONNECTION, data)
        return json.loads(resp.content)

    def get_connections(self, id):
        logging.info("[get_connections] id=%s", id)
        data = {"id": id}
        resp = self.post(common.PATHS.GET_CONNECTIONS, data)
        return json.loads(resp.content)
