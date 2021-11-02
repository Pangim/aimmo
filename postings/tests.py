import json
import jwt
import bcrypt

from django.test import TestCase, Client
from my_settings import ALGORITHM, SECRET_KEY
from users.models import User
from postings.models import Category, Posting

class PostingView(TestCase):
    def setUP(self):
        self.password = bcrypt.hashpw('12345678'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')        

        User.objects.create(
            id       = 1,
            name     = 'H',
            email    = 'a@naver.com',
            password = self.password,
        )
        User.objects.create(
            id       = 2,
            name     = 'A',
            email    = 'b@naver.com',
            password = self.password,
        ),
        User.objects.create(
            id       = 3,
            name     = 'J',
            email    = 'c@naver.com',
            password = self.password,
        )
        User.objects.create(
            id       = 4,
            name     = 'J',
            email    = 'd@naver.com',
            password = self.password,
        )
        
        Category.objects.create(
            id   = 1,
            name = 'soccer',
        )
        Category.objects.create(
            id   = 2,
            name = 'baseball',
        )

        Category.objects.create(
            id   = 3,
            name = 'basketball'
        )

        Posting.objects.create(
            id       = 1,
            category = 1,
            title    = 'messi',
            content  = 'Goal, Assist',
        )
        Posting.objects.create(
            id       = 2,
            category = 1,
            title    = 'ronaldo',
            content  = 'Goal, Assist',
        )
        Posting.objects.create(
            id       = 3,
            category = 1,
            title    = 'Agurero',
            content  = 'Goal, Assist',
        )
        Posting.objects.create(
            id       = 4,
            category = 2,
            title    = 'John',
            content  = 'Hit, Run',
        )
        Posting.objects.create(
            id       = 5,
            category = 2,
            title    = 'Jake',
            content  = 'Hit, Run',
        )
        Posting.objects.create(
            id       = 6,
            category = 2,
            title    = 'Jim',
            content  = 'Hit, Run',
        )

    def tearDown(self):
        User.objects.all().delete()
        Category.objects.all().delete()
        Posting.objects.all().delete()

    def test_posting_post_sucess(self):
        client = Client()

        User.objects.create(
           id       =  1,
           name     = 'H',
           email    = 'd@naver.com',
           password = bcrypt.hashpw('12345678'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

        Category.objects.create(
            id   = 3,
            name = 'basketball'
        )

        signin_user = {
            'email' : 'd@naver.com',
            'password' : '12345678'
        }
        signin_response = client.post('/users/signin', json.dumps(signin_user), content_type = 'application/json')

        data = {
            "title" : "messi",
            "content" : "Goal!!!!",
            "category_id" : 3,
        }

        headers = { "HTTP_Authorization" : signin_response.json()['access_token']}
        response = client.post("/postings", json.dumps(data), content_type = "application/json", **headers)
        
        self.maxDiff = None 
        self.assertEqual(response.json(), {
            "message" : "CREATED"
        })
        self.assertEquals(response.status_code, 201)
    
    def test_posting_post_fail_key_error(self):
        User.objects.create(
           id       =  1,
           name     = 'H',
           email    = 'd@naver.com',
           password = bcrypt.hashpw('12345678'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

        client = Client()

        signin_user = {
            'email' : 'd@naver.com',
            'password' : '12345678'
        }
        signin_response = client.post('/users/signin', json.dumps(signin_user), content_type = 'application/json')

        data = {
            "titlea" : "messi",
            "content" : "Goal!!!!",
            "category_id" : 1,
        }

        headers = { "HTTP_Authorization" : signin_response.json()['access_token']}
        response = client.post("/postings", json.dumps(data), content_type = "application/json", **headers)
        
        self.maxDiff = None 
        self.assertEqual(response.json(), {
            "message" : "KEY_ERROR"
        })
        self.assertEquals(response.status_code, 400)

    def test_posting_post_fail_does_not_exist(self):
        User.objects.create(
           id       =  1,
           name     = 'H',
           email    = 'd@naver.com',
           password = bcrypt.hashpw('12345678'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

        client = Client()

        signin_user = {
            'email' : 'd@naver.com',
            'password' : '12345678'
        }
        signin_response = client.post('/users/signin', json.dumps(signin_user), content_type = 'application/json')

        data = {
            "title" : "messi",
            "content" : "Goal!!!!",
            "category_id" : 100,
        }

        headers = { "HTTP_Authorization" : signin_response.json()['access_token']}
        response = client.post("/postings", json.dumps(data), content_type = "application/json", **headers)
        
        self.maxDiff = None 
        self.assertEqual(response.json(), {
            "message" : "CATEGORY_DOES_NOT_EXIST"
        })
        self.assertEquals(response.status_code, 400)

    def test_posting_patch_success(self):
        User.objects.create(
           id       =  1,
           name     = 'H',
           email    = 'd@naver.com',
           password = bcrypt.hashpw('12345678'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

        Category.objects.create(
            id = 1,
            name = "soccer"
        )

        Posting.objects.create(
            id = 1,
            title = "bird",
            content = "googoo",
            user_id = 1,
        )

        client = Client()

        signin_user = {
            'email' : 'd@naver.com',
            'password' : '12345678'
        }
        signin_response = client.post('/users/signin', json.dumps(signin_user), content_type = 'application/json')

        data = {
            "title" : "messi",
            "content" : "Goal!!!!",
            "category_id" : 1,
        }

        headers = { "HTTP_Authorization" : signin_response.json()['access_token']}
        response = client.patch("/postings/1", json.dumps(data), content_type = "application/json", **headers)
        
        self.maxDiff = None 
        self.assertEqual(response.json(), {
            "message" : "UPDATED"
        })
        self.assertEquals(response.status_code, 200)

    def test_posting_patch_fail_forbidden(self):
        User.objects.create(
           id       =  1,
           name     = 'H',
           email    = 'd@naver.com',
           password = bcrypt.hashpw('12345678'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

        Category.objects.create(
            id = 1,
            name = "soccer"
        )

        Posting.objects.create(
            id = 1,
            title = "bird",
            content = "googoo",
            user_id = 3,
        )

        client = Client()

        signin_user = {
            'email' : 'd@naver.com',
            'password' : '12345678'
        }
        signin_response = client.post('/users/signin', json.dumps(signin_user), content_type = 'application/json')

        data = {
            "title" : "messi",
            "content" : "Goal!!!!",
            "category_id" : 1,
        }

        headers = { "HTTP_Authorization" : signin_response.json()['access_token']}
        response = client.patch("/postings/1", json.dumps(data), content_type = "application/json", **headers)

        self.maxDiff = None 
        self.assertEqual(response.json(), {
            "message" : "FORBIDDEN"
        })
        self.assertEquals(response.status_code, 403)

    def test_posting_delete_success(self):
        User.objects.create(
           id       =  1,
           name     = 'H',
           email    = 'd@naver.com',
           password = bcrypt.hashpw('12345678'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

        Category.objects.create(
            id = 1,
            name = "soccer"
        )

        Posting.objects.create(
            id = 1,
            title = "bird",
            content = "googoo",
            user_id = 1
        )

        client = Client()

        signin_user = {
            'email' : 'd@naver.com',
            'password' : '12345678'
        }
        signin_response = client.post('/users/signin', json.dumps(signin_user), content_type = 'application/json')

        # data = {
        #     "title" : "messi",
        #     "content" : "Goal!!!!",
        #     "category_id" : 1,
        # }

        header = { "HTTP_Authorization" : signin_response.json()['access_token']}
        response = client.delete("/postings/1", content_type = "application/json", **header)
        print(response)

        self.maxDiff = None 
        self.assertEquals(response.status_code, 204)

    def test_posting_delete_fail_forbidden(self):
        User.objects.create(
           id       =  1,
           name     = 'H',
           email    = 'd@naver.com',
           password = bcrypt.hashpw('12345678'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

        Category.objects.create(
            id = 1,
            name = "soccer"
        )

        Posting.objects.create(
            id = 1,
            title = "bird",
            content = "googoo",
            user_id = 2,
        )

        client = Client()

        signin_user = {
            'email' : 'd@naver.com',
            'password' : '12345678'
        }
        signin_response = client.post('/users/signin', json.dumps(signin_user), content_type = 'application/json')

        # data = {
        #     "title" : "messi",
        #     "content" : "Goal!!!!",
        #     "category_id" : 1,
        # }

        header = { "HTTP_Authorization" : signin_response.json()['access_token']}
        response = client.delete("/postings/2", content_type = "application/json", **header)

        self.maxDiff = None 
        self.assertEqual(response.json(), {
            "message" : "POSTING_DOES_NOT_EXIST"
        })
        self.assertEquals(response.status_code, 400)

    def test_posting_delete_fail_does_not_exist(self):
        User.objects.create(
           id       =  1,
           name     = 'H',
           email    = 'd@naver.com',
           password = bcrypt.hashpw('12345678'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

        Category.objects.create(
            id = 1,
            name = "soccer"
        )

        Posting.objects.create(
            id = 1,
            title = "bird",
            content = "googoo",
            user_id = 2,
        )

        client = Client()

        signin_user = {
            'email' : 'd@naver.com',
            'password' : '12345678'
        }
        signin_response = client.post('/users/signin', json.dumps(signin_user), content_type = 'application/json')

        # data = {
        #     "title" : "messi",
        #     "content" : "Goal!!!!",
        #     "category_id" : 1,
        # }

        header = { "HTTP_Authorization" : signin_response.json()['access_token']}
        response = client.delete("/postings/1", content_type = "application/json", **header)

        self.maxDiff = None 
        self.assertEqual(response.json(), {
            "message" : "FORBIDDEN"
        })
        self.assertEquals(response.status_code, 403)

class PostingListView(TestCase):
    def setUP(self):
        User.objects.create(
            id       = 1,
            name     = 'H',
            email    = 'a@naver.com',
            password = self.password,
        )
        User.objects.create(
            id       = 2,
            name     = 'A',
            email    = 'b@naver.com',
            password = self.password,
        ),
        User.objects.create(
            id       = 3,
            name     = 'J',
            email    = 'c@naver.com',
            password = self.password,
        )
        User.objects.create(
            id       = 4,
            name     = 'J',
            email    = 'd@naver.com',
            password = self.password,
        )
        Category.objects.create(
            id   = 1,
            name = 'soccer',
        )
        Category.objects.create(
            id   = 2,
            name = 'baseball',
        )
        Category.objects.create(
            id   = 3,
            name = 'basketball'
        )
        Posting.objects.create(
            id       = 1,
            category = 1,
            title    = 'messi',
            content  = 'Goal, Assist',
        )
        Posting.objects.create(
            id       = 2,
            category = 1,
            title    = 'ronaldo',
            content  = 'Goal, Assist',
        )
        Posting.objects.create(
            id       = 3,
            category = 1,
            title    = 'Agurero',
            content  = 'Goal, Assist',
        )
        Posting.objects.create(
            id       = 4,
            category = 2,
            title    = 'John',
            content  = 'Hit, Run',
        )
        Posting.objects.create(
            id       = 5,
            category = 2,
            title    = 'Jake',
            content  = 'Hit, Run',
        )
        Posting.objects.create(
            id       = 6,
            category = 2,
            title    = 'Jim',
            content  = 'Hit, Run',
        )

    def tearDown(self):
        User.objects.all().delete()
        Category.objects.all().delete()
        Posting.objects.all().delete()

    def test_posting_list_post_sucess(self):
        client = Client()

        response = client.get("/postings/list", content_type = "application/json")

        self.maxDiff = None
        self.assertEquals(response.status_code, 200)