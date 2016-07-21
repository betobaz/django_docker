from django.test import RequestFactory

from test_plus.test import TestCase

import requests_mock


from ..views import (
    SignupView
)

class TestSingupView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_get_view(self):
        response = self.client.get('/portal/signup/')
        self.assertEqual(response.status_code, 200)

    def test_form_view(self):
        response = self.client.get('/portal/signup/')
        self.assertContains(response, 
            '<form' # Contiene el formulario de singup
        )

    def test_post_form(self):
        url = 'https://merxbp.sugarondemand.com/'
        sugar_endpoint = '{0}/rest/v10/oauth2/token'.format(url)
        request = self.factory.post('/portal/signup/', {
            'instance_url': url,
            'client_id': 'client id',
            'client_secret': 'client secret',
            'username': 'username',
            'password': 'password',
        })

        adapter = requests_mock.Adapter()
        json_response = {
            'access_token':'123',
            'refresh_token':'123',
        }
        adapter.register_uri('POST', sugar_endpoint, json=json_response)

        response = SignupView.as_view()(request)
        self.assertEqual(response.status_code, 200)

        # self.assertContains(response.content, 
        #     'No Responde sugar :(' # Contiene el formulario de singup
        # )
