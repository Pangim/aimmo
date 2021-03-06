import json
import jwt
import bcrypt

from django.http     import response
from django.test import TestCase, Client

from users.models import User
from postings.models import Category, Posting, Comment
from my_settings     import ALGORITHM, SECRET_KEY

class PostingsAppTest(TestCase):
    def setUp(self):
        category_id = Category.objects.create(id=1, name='test').id
        
        user_list = [
            User(
                id       = 1,
                name     = 'test',
                email    = 'wanted1@wecode.com',
                password = 'wantedwecode1'
            ),
            User(
                id       = 2,
                name     = 'test',
                email    = 'wanted2@wecode.com',
                password = 'wantedwecode2'
            ),
            User(
                id       = 3,
                name     = 'test',
                email    = 'wanted3@wecode.com',
                password = 'wantedwecode3'
            ),
            User(
                id       = 4,
                name     = 'test',
                email    = 'wanted4@wecode.com',
                password = 'wantedwecode4'
            ),
            User(
                id       = 5,
                name     = 'test',
                email    = 'wanted5@wecode.com',
                password = 'wantedwecode5'
            ),
            User(
                id       = 6,
                name     = 'test',
                email    = 'wanted6@wecode.com',
                password = 'wantedwecode6'
            ),
            User(
                id       = 7,
                name     = 'test',
                email    = 'wanted7@wecode.com',
                password = 'wantedwecode7'
            ),
            User(
                id       = 8,
                name     = 'test',
                email    = 'wanted8@wecode.com',
                password = 'wantedwecode8'
            ),
            User(
                id       = 9,
                name     = 'test',
                email    = 'wanted9@wecode.com',
                password = 'wantedwecode9'
            ),
            User(
                id       = 10,
                name     = 'test',
                email    = 'wanted10@wecode.com',
                password = 'wantedwecode10'
            )
        ]
        User.objects.bulk_create(user_list)

        posting_list = [
            Posting(
                id          = 1,
                category_id = category_id,
                user_id     = 1,
                title       = 'title1',
                views       = 1,
                content     = 'content1'
            ),
            Posting(
                id          = 2,
                category_id = category_id,
                user_id     = 2,
                title       = 'title2',
                views       = 2,
                content     = 'content2'
            ),
            Posting(
                id          = 3,
                category_id = category_id,
                user_id     = 3,
                title       = 'title3',
                views       = 3,
                content     = 'content3'
            ),
            Posting(
                id          = 4,
                category_id = category_id,
                user_id     = 4,
                title       = 'title4',
                views       = 4,
                content     = 'content4'
            ),
            Posting(
                id          = 5,
                category_id = category_id,
                user_id     = 5,
                title       = 'title5',
                views       = 5,
                content     = 'content5'
            ),
            Posting(
                id          = 6,
                category_id = category_id,
                user_id     = 6,
                title       = 'title6',
                views       = 6,
                content     = 'content6'
            ),
            Posting(
                id          = 7,
                category_id = category_id,
                user_id     = 7,
                title       = 'title7',
                views       = 7,
                content     = 'content7'
            ),
            Posting(
                id          = 8,
                category_id = category_id,
                user_id     = 8,
                title       = 'title8',
                views       = 8,
                content     = 'content8'
            ),
            Posting(
                id          = 9,
                category_id = category_id,
                user_id     = 9,
                title       = 'title9',
                views       = 9,
                content     = 'content9'
            ),
            Posting(
                id          = 10,
                category_id = category_id,
                user_id     = 10,
                title       = 'title10',
                views       = 10,
                content     = 'content10'
            )
        ]
        Posting.objects.bulk_create(posting_list)

        comment_list = [
            Comment(
                id                = 1,
                posting_id        = 1,
                user_id           = 1,
                parent_comment_id = None,
                content           = 'comment_test'
            ),
            Comment(
                id                = 2,
                posting_id        = 2,
                user_id           = 2,
                parent_comment_id = None,
                content           = 'comment_test'
            ),
            Comment(
                id                = 3,
                posting_id        = 3,
                user_id           = 3,
                parent_comment_id = None,
                content           = 'comment_test'
            ),
            Comment(
                id                = 4,
                posting_id        = 4,
                user_id           = 4,
                parent_comment_id = None,
                content           = 'comment_test'
            ),
            Comment(
                id                = 5,
                posting_id        = 5,
                user_id           = 5,
                parent_comment_id = None,
                content           = 'comment_test'
            ),
            Comment(
                id                = 6,
                posting_id        = 6,
                user_id           = 6,
                parent_comment_id = None,
                content           = 'comment_test'
            ),
            Comment(
                id                = 7,
                posting_id        = 7,
                user_id           = 7,
                parent_comment_id = None,
                content           = 'comment_test'
            ),
            Comment(
                id                = 8,
                posting_id        = 8,
                user_id           = 8,
                parent_comment_id = None,
                content           = 'comment_test'
            ),
            Comment(
                id                = 9,
                posting_id        = 9,
                user_id           = 9,
                parent_comment_id = None,
                content           = 'comment_test'
            ),
            Comment(
                id                = 10,
                posting_id        = 10,
                user_id           = 10,
                parent_comment_id = None,
                content           = 'comment_test'
            )
        ]

        nested_comment_list=[    
            Comment(
                id                = 11,
                posting_id        = 1,
                user_id           = 1,
                parent_comment_id = 1,
                content           = 'comment_test'
            ),
            Comment(
                id                = 12,
                posting_id        = 1,
                user_id           = 2,
                parent_comment_id = 1,
                content           = 'comment_test'
            ),
            Comment(
                id                = 13,
                posting_id        = 1,
                user_id           = 3,
                parent_comment_id = 1,
                content           = 'comment_test'
            ),
            Comment(
                id                = 14,
                posting_id        = 1,
                user_id           = 4,
                parent_comment_id = 1,
                content           = 'comment_test'
            ),
            Comment(
                id                = 15,
                posting_id        = 1,
                user_id           = 5,
                parent_comment_id = 1,
                content           = 'comment_test'
            ),
            Comment(
                id                = 16,
                posting_id        = 1,
                user_id           = 6,
                parent_comment_id = 2,
                content           = 'comment_test'
            ),
            Comment(
                id                = 17,
                posting_id        = 1,
                user_id           = 7,
                parent_comment_id = 2,
                content           = 'comment_test'
            ),
            Comment(
                id                = 18,
                posting_id        = 1,
                user_id           = 8,
                parent_comment_id = 2,
                content           = 'comment_test'
            ),
            Comment(
                id                = 19,
                posting_id        = 1,
                user_id           = 9,
                parent_comment_id = 2,
                content           = 'comment_test'
            ),
            Comment(
                id                = 20,
                posting_id        = 1,
                user_id           = 10,
                parent_comment_id = 2,
                content           = 'comment_test'
            ),
        ]
        Comment.objects.bulk_create(comment_list)
        Comment.objects.bulk_create(nested_comment_list)

    def tearDown(self):
        Category.objects.all().delete()
        Posting.objects.all().delete()
        Comment.objects.all().delete()

    def test_success_post_comment(self):
        client       = Client()
        headers      = {'HTTP_Authorization' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.bnePFYer6pRlx7yiOa4UGcKdL2I65VhjAYpEc8jaG1s'}
        comment_info = {
            'parnt-comment_id' : 1,
            'posting_id'       : 1,
            'user_id'          : 1,
            'content'          : 'content test'
        }
        response = client.post('/postings/comments/1', json.dumps(comment_info), content_type='application/json',**headers)
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.json(),{
            'message':'SUCCESS'
        })
    
    def test_success_post_comment_posting_does_not_exist(self):
        client       = Client()
        headers      = {'HTTP_Authorization' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.bnePFYer6pRlx7yiOa4UGcKdL2I65VhjAYpEc8jaG1s'}
        comment_info = {
            'parent_comment_id' : None,
            'posting_id'        : 50,
            'user_id'           : 1,
            'content'           : 'content test'
        }
        response = client.post('/postings/comments/50', json.dumps(comment_info), content_type='application/json',**headers)
        self.assertEqual(response.status_code,404)
        self.assertEqual(response.json(),{
            'message':'POSTING_DOES_NOT_EXIST'
        })
    
    def test_success_get_comments(self):
        client   = Client()
        response = client.get('/postings/comments/1?offset=0&limit=5')
        self.assertEqual(response.status_code,200)
    
    def test_success_get_commemts_postings_does_not_exist(self):
        client   = Client()
        response = client.get('/postings/comments/40?offset=0&limit=5')
        self.assertEqual(response.status_code,404)
        self.assertEqual(response.json(),{
            'message': 'POSTING_DOES_NOT_EXIST'
        })
    
    def test_success_delete_comment(self):
        client   = Client()
        headers  = {'HTTP_Authorization' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.bnePFYer6pRlx7yiOa4UGcKdL2I65VhjAYpEc8jaG1s'}
        response = client.delete('/postings/comments?id=1',**headers)
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.json(),{
            'message':'SUCCESS'
        })

    def test_success_delete_comment_invalid_user(self):
        client   = Client()
        headers  = {'HTTP_Authorization' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.bnePFYer6pRlx7yiOa4UGcKdL2I65VhjAYpEc8jaG1s'}
        response = client.delete('/postings/comments?id=5',**headers)
        self.assertEqual(response.status_code,401)
        self.assertEqual(response.json(),{
            'message' : 'INVALID_USER'
        })
    
    def test_success_update_comment(self):
        client       = Client()
        headers      = {'HTTP_Authorization' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.bnePFYer6pRlx7yiOa4UGcKdL2I65VhjAYpEc8jaG1s'}
        comment_info = {
            'id'         : 1,
            'posting_id' : 1,
            'user_id'    : 1,
            'content'    : 'content test'
        }
        response = client.patch('/postings/comments?id=1',json.dumps(comment_info), content_type='application/json',**headers)
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.json(),{
            'message':'SUCCESS'
        })

    def test_success_update_comment_invalid_user(self):
        client       = Client()
        headers      = {'HTTP_Authorization' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.bnePFYer6pRlx7yiOa4UGcKdL2I65VhjAYpEc8jaG1s'}
        comment_info = {
            'parent_comment_id' : 1,
            'posting_id'        : 1,
            'user_id'           : 1,
            'content'           : 'content test'
        }
        response = client.patch('/postings/comments?id=10',json.dumps(comment_info), content_type='application/json',**headers)
        self.assertEqual(response.status_code,401)
        self.assertEqual(response.json(),{
            'message' : 'INVALID_USER'
        }
        )

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
