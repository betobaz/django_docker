from django.test import RequestFactory

from test_plus.test import TestCase

import requests_mock

from ..forms import SignUpForm

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





