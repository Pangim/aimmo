import json
import bcrypt
import jwt

from django.http    import JsonResponse
from django.views   import View

from users.models   import User
from aimmo.settings import SECRET_KEY, ALGORITHM

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({"message": "DUPLICATED_EMAIL"}, status=400)

            encode_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            decode_password = encode_password.decode('utf-8')

            User.objects.create(
                name     = data['name'],
                password = decode_password,
                email    = data['email']
            )

        except KeyError:
            return JsonResponse({"message": "KEYERROR"}, status=400)
        
        return JsonResponse({"message": "CREATED!"}, status=201)
    
class SigninView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            user = User.objects.get(email = data['email'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message": "LOGIN FAILED!"}, status=401)

            access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
        
        except KeyError:
            return JsonResponse({"message": "KEYERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message": "LOGIN FAILED!"}, status=401)
        
        return JsonResponse({"access_token": access_token}, status=201)