from django.test import RequestFactory

from test_plus.test import TestCase

import requests_mock


from ..views import (
    SignupView
)

requests_mock.Mocker.TEST_PREFIX = 'actio'

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

    @requests_mock.mock()
    def test_post_form(self, m):
        url = 'https://merxbp.sugarondemand.com/'
        sugar_endpoint = '{0}rest/v10/oauth2/token'.format(url)
        request = self.factory.post('/portal/signup/', {
            'instance_url': url,
            'client_id': 'client id',
            'client_secret': 'client secret',
            'username': 'username',
            'password': 'password',
        })

        json_response = {
            'access_token':'123',
            'refresh_token':'123',
        }
        m.post(sugar_endpoint, json=json_response)

        response = SignupView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/portal/signup-success/")

    @requests_mock.mock()
    def test_post_form_error(self, m):
        url = 'https://merxbp.sugarondemand.com/'
        sugar_endpoint = '{0}rest/v10/oauth2/token'.format(url)
        request = self.factory.post('/portal/signup/', {
            'instance_url': url,
            'client_id': 'client id',
            'client_secret': 'client secret',
            'username': 'username',
            'password': 'password',
        })

        json_response = {
            'access_token':'123',
            'refresh_token':'123',
        }
        m.post(sugar_endpoint, json=json_response, status_code=400)

        response = SignupView.as_view()(request)
        # print (response.content)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "No Responde sugar :(")
