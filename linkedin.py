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


l = LinkedIn()
# get a new authorization code before running this
accessToken = l.getAccessToken('AQR_6NYaGVqtX2oYPWT23MoqIm46v8CuG89IQgZk9VW-A3nJSI1lwk5tc0YIeDGo0HR_cyBQu23pSetiYRV1gUeKfOani0h6tKbxxe_RSVYcykKBqedWrWWvmM-PWeMtE9R9ziG_t8b9EIGWbw-i8nMAyeJjZbFBzdK0nOydENzbTILLegTwM_678dwaQg')
# print(accessToken)
print(l.getProfile(accessToken))
exit(1)

API_KEY = '78m2wtjn8oc8ok'
API_SECRET = 'WNNz6KpUYxcuGmAD'
# LinkedIn redirects the user back to your website's URL after granting access (giving proper permissions) to your application
RETURN_URL = 'http://localhost:8000'


application = linkedin.LinkedInApplication(token='AQVT6PsIEf4tBEsqCWHNIvR6EIY3LHGx4h8q4mWMDb4SG_e5Pbsw27aobYrw1IfCMnY0D9_QsKAn_OvQA-zs1OlupEoVNHwIuBtOAKf_g5RicBofkW3C9ZfOyOHhQdl3_pmL4tvRchcgfaXRVr2oRmzwvvkm6UuR7ZvGSKF3wLZ7D3nfi8MQcB8BbuCH5NuSp3_CuFn-UFAMKeJ0ySVEn93qJO2HsfhEA9xxjULLnysWkTcMIwNnljfuNGf9fm3l8fzrN7eR-ekE0yUnxhRhBIOMPPZDEVIJXyxdEaWoxuVc-nMOULSiysqOhcH3Dv3YkTHO35rfRlw-SddJhJB5t55j8iX51w')
print(application.get_profile())
# application.get_connections()

