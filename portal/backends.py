from actio_control.users.models import User
from .models import Instance
from .lib.sugarcrm_api_py.SugarCRMAPI import SugarCRMAPI 

class ActioBackend(object):

    def authenticate(self, url=None, username=None, password=None):
        try:
            print("ActioBackend:authenticate: url:{0}".format(url))
            print("ActioBackend:authenticate: username:{0}".format(username))
            print("ActioBackend:authenticate: password:{0}".format(password))
            
            instance = Instance.objects.get(url=url)
            print("ActioBackend:authenticate: Hay instancia")
            user = User.objects.get(instance=instance, sugar_username=username)
            print("ActioBackend:authenticate: Hay instancia")

            sugar_api = SugarCRMAPI(
                instance.url, 
                instance.client_id, 
                instance.client_secret
            )

            tokens = sugar_api.oauth2_token(
                username, 
                password
            )

            if tokens['status_code'] == 200 :
                user.access_token = tokens['response_dic']['access_token'] 
                user.refresh_token = tokens['response_dic']['refresh_token']
                user.save()
            else:
                user = None

        except Instance.DoesNotExist:
            user = None

        except User.DoesNotExist:
            user = None
        return user

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None

        
