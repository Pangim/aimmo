import jwt

from django.http import JsonResponse

from users.models import User
from my_settings  import SECRET_KEY, ALGORITHM

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = jwt.decode(request.headers.get('Authorization'), SECRET_KEY, algorithms=ALGORITHM)
            user         = User.objects.get(id = access_token['id'])
            request.user = user

        except User.DoesNotExist:
            return JsonResponse({'message' : 'USER_DOES_NOT_EXIST'}, status = 400)

        except jwt.DecodeError:
            return JsonResponse({'message' : 'UNKNOWN_USER'}, status = 400)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message' : 'EXPIRED_TOKEN'}, status = 400)

        return func(self, request, *args, **kwargs)
    
    return wrapper