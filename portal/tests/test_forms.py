from django.test import RequestFactory

from test_plus.test import TestCase

import requests_mock

from ..forms import (
    SignUpForm,
    SignInForm
)

from ..models import Instance
from actio_control.users.models import User


requests_mock.Mocker.TEST_PREFIX = 'actio'

class TestSingupForm(TestCase):

    def tearDown(self):
        Instance.objects.all().delete()
        User.objects.all().delete()

    def test_get_instance_exist(self):
        url = 'https://merxbp.sugarondemand.com/'
        instance = Instance(
            url=url
            )
        instance.save()

        form = SignUpForm({
            'instance_url': url,
            'client_id': 'client id',
            'client_secret': 'client secret',
            'username': 'username',
            'password': 'password',
        })
        form.is_valid()
        instance = form.create_instance()
        self.assertEqual(len(Instance.objects.all()), 1)

    def test_get_user_exist(self):
        url = 'https://merxbp.sugarondemand.com/'
        instance = Instance(
            url=url
            )
        instance.save()

        user = User(
            sugar_username='admin',
            sugar_id='user_id_123',
            instance=instance
        )
        user.save()

        form = SignUpForm({
            'instance_url': url,
            'client_id': 'client id',
            'client_secret': 'client secret',
            'username': 'admin',
            'password': 'password',
        })
        form.is_valid()
        
        tokens = {
            'response_dic': {
                'access_token':'access_token_123',
                'refresh_token':'refresh_token_123',
            }
        }
        me = {
            'current_user': {
                'id': 'user_id_123'
            } 
        }

        user = form.create_user(tokens, me, instance)
        self.assertEqual(len(User.objects.all()), 1)

class TestSignInForm(TestCase):

    def setUp(self):
        self.url = 'https://merxbp.sugarondemand.com/'
        self.form = SignInForm({
            'instance_url': self.url,
            'username': 'admin',
            'password': 'password',
        })
        self.form.is_valid()

    def tearDown(self):
        Instance.objects.all().delete()
        User.objects.all().delete()

    def test_fields(self):
        self.assertTrue(self.form.fields['instance_url'])
        self.assertTrue(self.form.fields['username'])
        self.assertTrue(self.form.fields['password'])

    @requests_mock.mock()
    def test_login_not_exist_instance(self,m):
        with self.assertRaises(Instance.DoesNotExist):
            self.form.login()

    @requests_mock.mock()
    def test_login_not_exist_user(self,m):
        instance = Instance(
            url=self.url
        )
        instance.save()

        with self.assertRaises(User.DoesNotExist):
            self.form.login()

    @requests_mock.mock()
    def test_login_request(self,m):
        sugar_endpoint_token = '{0}rest/v10/oauth2/token'.format(self.url)
        json_response_token = {
            'access_token':'access_token_123',
            'refresh_token':'refresh_token_123',
        }
        m.post(sugar_endpoint_token, json=json_response_token)

        instance = Instance(
            url=self.url
        )
        instance.save()
        user = User(
            sugar_username='admin',
            sugar_id='user_id_123',
            instance=instance,
            access_token='access_toke_321'
        )
        user.save()

        self.form.login()
        self.assertTrue(m.called)

        history = m.request_history

        self.assertEqual("POST", history[0].method)
        self.assertEqual(sugar_endpoint_token, history[0].url)

        user.refresh_from_db()
        self.assertEqual('access_token_123', user.access_token)

    # @requests_mock.mock()
    # def test_login_request_error(self,m):
    #     sugar_endpoint_token = '{0}rest/v10/oauth2/token'.format(self.url)
    #     json_response_token = {
    #         'access_token':'access_token_123',
    #         'refresh_token':'refresh_token_123',
    #     }
    #     m.post(sugar_endpoint_token, json=json_response_token, status_code=400)

    #     instance = Instance(
    #         url=self.url
    #     )
    #     instance.save()
    #     user = User(
    #         sugar_username='admin',
    #         sugar_id='user_id_123',
    #         instance=instance
    #     )
    #     user.save()

    #     self.form.login()
    #     self.assertTrue(m.called)

    #     history = m.request_history

    #     self.assertEqual("POST", history[0].method)
    #     self.assertEqual(sugar_endpoint_token, history[0].url)






