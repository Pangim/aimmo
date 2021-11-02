import jwt
import bcrypt
import json

from django.test  import TestCase, Client

from users.models import User
from my_settings  import SECRET_KEY, ALGORITHM

class Test(TestCase):
    def setUp(self):
        self.password = bcrypt.hashpw("ko122!".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        User.objects.bulk_create([
            User(
                id       = 1,
                name     = "김코딩",
                email    = "kim12@naver.com",
                password = self.password
            ),
            User(
                id       = 2,
                name     = "김코드",
                email    = "code12@naver.com",
                password = "code5500"
            ),
            User(
                id       = 3,
                name     = "박부자",
                email    = "money11@gmail.com",
                password = "lovemoney123"
            ),
            User(
                id       = 4,
                name     = "노션킴",
                email    = "notion@naver.com",
                password = "zxxx441!@@"
            ),
            User(
                id       = 5,
                name     = "유슬랙",
                email    = "slack@gmail.com",
                password = "slack122!"
            )
        ])

        self.access_token = jwt.encode({"id": 1}, SECRET_KEY, algorithm=ALGORITHM)

    def tearDown(self):
        User.objects.all().delete()
    
    def test_post_success_signup(self):
        client = Client()
        data   = {
            "name"     : "코딩",
            "password" : "codeking123",
            "email"    : "code22@naver.com"
        }
        response = client.post('/users/signup', json.dumps(data), content_type='applications/json')

        self.assertEqual(response.json(),
            {
                "message": "CREATED!"
            }
        )
        self.assertEquals(response.status_code, 201)
    
    def test_post_fail_signup_keyerror(self):
        client   = Client()
        data     = {}
        response = client.post('/users/signup', json.dumps(data), content_type='applications/json')

        self.assertEqual(response.json(),
            {
                "message": "KEYERROR"
            }
        )
        self.assertEquals(response.status_code, 400)
    
    def test_post_fail_signup_duplicated_email(self):
        client = Client()
        data   = {
            "name"     : "코딩",
            "password" : "codeking123",
            "email"    : "kim12@naver.com"
        }
        response = client.post('/users/signup', json.dumps(data), content_type='applications/json')

        self.assertEqual(response.json(),
            {
                "message": "DUPLICATED_EMAIL"
            }
        )
        self.assertEquals(response.status_code, 400)

    def test_post_success_signin(self):
        client = Client()
        data   = {
            "email"    : "kim12@naver.com",
            "password" : "ko122!"
        }
        response = client.post('/users/signin', json.dumps(data), content_type='applications/json')
        user     = User.objects.get(email = data['email'])

        if bcrypt.checkpw(data["password"].encode('utf-8'), self.password.encode('utf-8')):
            access_token = jwt.encode({"id": user.id}, SECRET_KEY, algorithm=ALGORITHM)
        
        self.assertEqual(response.json(),
            {
                "access_token": access_token
            }
        )
        self.assertEquals(response.status_code, 201)
    
    def test_post_fail_signin_do_not_exist_user(self):
        client = Client()
        data   = {
            "email"    : "coco@naver.com",
            "password" : "coco2@@"
        }
        response = client.post('/users/signin', json.dumps(data), content_type='applications/json')
        
        User.objects.filter(email = data['email']).distinct()
        
        self.assertEqual(response.json(),
            {
                "message": "DO NOT EXIST!"
            }
        )
        self.assertEquals(response.status_code, 401)
    
    def test_post_fail_signin_input_wrong_password(self):
        client = Client()
        data   = {
            "email"    : "김코딩",
            "password" : "coco2@@"
        }
        response = client.post('/users/signin', json.dumps(data), content_type='applications/json')
        
        if not bcrypt.checkpw(data["password"].encode('utf-8'), self.password.encode('utf-8')):
        
            self.assertEqual(response.json(),
                {
                    "message": "DO NOT EXIST!"
                }
            )
            self.assertEquals(response.status_code, 401)
    
    def test_post_fail_signin_keyerror(self):
        client   = Client()
        data     = {}
        response = client.post('/users/signin', json.dumps(data), content_type='applications/json')

        self.assertEqual(response.json(),
            {
                "message": "KEYERROR"
            }
        )
        self.assertEquals(response.status_code, 400)
