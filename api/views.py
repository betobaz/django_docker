from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from portal.lib.sugarcrm_api_py.SugarCRMAPI import SugarCRMAPI 
from portal.models import Instance
from actio_control.users.models import User

class TestView(APIView):
    def get(self, request, format=None):
        return Response({'saludo': 'Hola mundo'})

class LoginView(APIView):
    def post(self, request, format=None):
        instance = Instance.objects.get(url=request.data['url'])
        user = User.objects.get(instance=instance, sugar_username=request.data['username'])
        sugar_api = SugarCRMAPI(
            instance.url, 
            instance.client_id, 
            instance.client_secret
        )
        tokens = sugar_api.oauth2_token(
            request.data['username'], 
            request.data['password']
        )

        if tokens['status_code'] == 200 :
            user.access_token = tokens['response_dic']['access_token'] 
            user.refresh_token = tokens['response_dic']['refresh_token']
            user.save()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)            

        return Response({'user': user.id})

class SearchView(APIView):
    def get(self, request, format=None):
        result = {}
        try:
            user_id = request.META.get('HTTP_USER_ID')
            q = request.GET.get('q')
            if user_id :
                user = User.objects.get(id=user_id)
                sugar_api = SugarCRMAPI(
                    user.instance.url, 
                    user.instance.client_id, 
                    user.instance.client_secret
                )
                sugar_api.set_token(user.access_token)
                sugar_api.set_refresh_token(user.refresh_token)
                print("globalsearch?tags=false&q={0}&fields=id,name".format(q))
                result = sugar_api.call("get", "globalsearch?tags=false&q={0}".format(q))
        except MultiValueDictKeyError:
            result = {} 
        return Response({'result': result})