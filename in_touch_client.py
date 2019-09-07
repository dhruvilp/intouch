import requests
from exceptions import ClientRequestException, InvalidEnvException
import common
import logging

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

    def new_user(self, id, name):
        logging.info("[new_user] id=%s, name=%s" % (id, name))
        data = dict(id=id, name=name)
        self.post(common.PATHS.NEW_USER, data)