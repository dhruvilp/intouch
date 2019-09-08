from linkedin_v2 import linkedin
import requests
import json

class LinkedIn:
    
    def __init__(self):
        self.api_id = '78m2wtjn8oc8ok'
        self.api_secret = 'WNNz6KpUYxcuGmAD'


    def getAccessToken(self, auth_code):
        headers = {'content-type': 'application/json'}
        url = 'https://www.linkedin.com/oauth/v2/accessToken'
        
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_id,
            "client_secret": self.api_secret
        }
        
        params = {
            'client_id': self.api_id,
            'grant_type': 'authorization_code',
            'client_secret': self.api_secret,
            'redirect_uri': 'https://www.linkedin.com/oauth/v2/authorization',
            'code': auth_code
        }

        r = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        return r.json()['access_token']


    def getProfile(self, accessToken):
        app = linkedin.LinkedInApplication(token=accessToken)
        return app.get_profile()

