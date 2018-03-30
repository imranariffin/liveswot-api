import json

from django.urls import reverse


def setupToken(self, client):

    auth_data = {
        'user': {
            'email': 'imran.ariffin@liveswot.com', 'password': 'katakunci'
        }
    }
    gettoken_response = client.post(
        reverse('authenticationjwt:login'),
        content_type="application/json",
        data=json.dumps(auth_data))

    client.credentials(
        HTTP_AUTHORIZATION='Bearer ' + gettoken_response.data['token']
    )

    self.token = gettoken_response.data['token']