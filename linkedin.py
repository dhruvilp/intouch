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
            'client_id':'78m2wtjn8oc8ok',
            'grant_type': 'authorization_code',
            'client_secret': 'WNNz6KpUYxcuGmAD',
            'redirect_uri': 'https://www.linkedin.com/oauth/v2/authorization',
            'code': auth_code
        }

        r = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        return r.json()['access_token'])


linkedin = LinkedIn()
# get a new authorization code before running this
linkedin.getAccessToken('AQRm99DdOesbeWnKMSwu45Bl_SeIq3Kpnw-prm6xS0KYe863mieJ7ABtXByP1GMqFne3p0qgEin5vd49p4PVMrL8yAM90ALyxz8L2iTz59ShBVrLogm_kFbpMT7w5T3dnZVMjC024HObdBI3ZSM8BLx16l35FlTw3CaW7izSZ8v0Fwh_sPqzWs8WftNTGg')