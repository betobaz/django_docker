from django.test import RequestFactory

from test_plus.test import TestCase

import requests_mock


from ..views import (
    SignupView
)

from ..models import (
    Instance
)

from actio_control.users.models import (
    User
)


requests_mock.Mocker.TEST_PREFIX = 'actio'

class TestSingupView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def tearDown(self):
        Instance.objects.all().delete()
        User.objects.all().delete()

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
        sugar_endpoint_me = '{0}rest/v10/me'.format(url)
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
        json_response_me = {
            "current_user":{
              "type":"admin",
              "id":"useradmin123",
              "user_name":"username"
            }
        }
        m.post(sugar_endpoint, json=json_response)
        m.get(sugar_endpoint_me, json=json_response_me)

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

    @requests_mock.mock()
    def test_post_create_instance_user(self, m):
        url = 'https://merxbp.sugarondemand.com/'
        sugar_endpoint_token = '{0}rest/v10/oauth2/token'.format(url)
        sugar_endpoint_me = '{0}rest/v10/me'.format(url)
        username = 'usertest' 
        request = self.factory.post('/portal/signup/', {
            'instance_url': url,
            'client_id': 'client id',
            'client_secret': 'client secret',
            'username': username,
            'password': 'password',
        })

        json_response_token = {
            'access_token':'access_token_123',
            'refresh_token':'refresh_token_123',
        }
        json_response_me = {
            "current_user":{
              "type":"admin",
              "id":"useradmin123",
              "user_name":username
            }
        }
        m.post(sugar_endpoint_token, json=json_response_token)
        m.get(sugar_endpoint_me, json=json_response_me)
        
        response = SignupView.as_view()(request)

        instance = Instance.objects.get(url=url)
        user = User.objects.get(sugar_username=username)
        self.assertTrue(instance)
        self.assertTrue(user)
        self.assertEqual(user.access_token, 'access_token_123')
        self.assertEqual(user.refresh_token, 'refresh_token_123')
        self.assertEqual(user.sugar_id, "useradmin123")
        self.assertEqual(user.sugar_type, "admin")
        self.assertTrue(user.instance)
        self.assertEqual(user.instance, instance)

