class InvalidEnvException(Exception):
    def __init__(self):
        self.message = "ENV must be one of DEV and PROD"

class ClientRequestException(Exception):
    def __init__(self, message):
        self.message = message