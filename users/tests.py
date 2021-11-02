import json, bcrypt

from django.test   import TestCase, Client
from unittest.mock import patch

from .models       import User
from my_settings   import ALGORITHM, SECRET_KEY

class SignUpTest(TestCase):
  def setUp(self):
    User.objects.bulk_create(
      [User(
        id       = 1,
        name     = '김민호',
        email    = 'rlaalsgh@gmail.com',
        password = 'rlaalsgh11!'
      ),
      User(
        id       = 2,
        name     = '김민우',
        email    = 'rlaalsdn@gmail.com',
        password = 'rlaalsdn11!'
      )]
    )

  def tearDown(self):
    User.objects.all().delete()

  def test_signup_success(self):
    client = Client()

    user = {
      'name'     : '박치훈',
      'email'    : 'qkrclgns@gmail.com',
      'password' : 'qkrclgns11!'
    }

    response = client.post('/users/signup', json.dumps(user), content_type = 'application/json')

    self.assertEqual(response.json(),{'MESSAGE' : 'SUCCESS'})
    self.assertEqual(response.status_code, 201)

  def test_signup_failure_invalid_email(self):
    client = Client()

    user = {
      'name'     : '박치훈',
      'email'    : 'qkrclgnsgamil.com',
      'password' : 'qkrclgns11!'
    }

    response = client.post('/users/signup', json.dumps(user), content_type = 'application/json')

    self.assertEqual(response.json(),{'MESSAGE' : 'INVALID_EMAIL'})
    self.assertEqual(response.status_code, 400)

  def test_signup_failure_invalid_password(self):
    client = Client()

    user = {
      'name'     : '박치훈',
      'email'    : 'qkrclgns@gmail.com',
      'password' : '123123123'
    }

    response = client.post('/users/signup', json.dumps(user), content_type = 'application/json')

    self.assertEqual(response.json(),{'MESSAGE' : 'INVALID_PASSWORD'})
    self.assertEqual(response.status_code, 400)

  def test_signup_failure_duplicated_email(self):
    client = Client()

    user = {
      'name'     : '박치훈',
      'email'    : 'rlaalsgh@gmail.com',
      'password' : 'rlaalsgh11!'
    }

    response = client.post('/users/signup', json.dumps(user), content_type = 'application/json')

    self.assertEqual(response.json(),{'MESSAGE' : 'DUPLICATED_EMAIL'})
    self.assertEqual(response.status_code, 409)

  def test_signup_failure_key_error(self):
    client = Client()

    user = {
      'name'     : '박치훈',
      'password' : 'qkrclgns11!'
    }

    response = client.post('/users/signup', json.dumps(user), content_type = 'application/json')

    self.assertEqual(response.json(),{'MESSAGE' : 'KEY_ERROR'})
    self.assertEqual(response.status_code, 400)


class SignInTest(TestCase):
  def setUp(self):
    hashed_password  = bcrypt.hashpw("rlaalsgh11!".encode('utf-8'), bcrypt.gensalt())
    decoded_password = hashed_password.decode('utf-8')

    user = User.objects.create(
      id       = 1,
      name     = '김민호',
      email    = 'rlaalsgh@gmail.com',
      password = decoded_password 
    )

  def tearDown(self):
    User.objects.all().delete()

  def test_signin_success(self):
    client = Client()

    user = {
      'email'    : 'rlaalsgh@gmail.com',
      'password' : 'rlaalsgh11!'
    }

    response = client.post('/users/signin', json.dumps(user), content_type = 'application/json')
    access_token = response.json()['ACCESS_TOKEN']

    self.assertEqual(response.json(),{'ACCESS_TOKEN' : access_token,})
    self.assertEqual(response.status_code, 200)

  def test_signin_failure_invalid_email(self):
    client = Client()

    user = {
      'email'    : 'rlaalsghgmail.com',
      'password' : 'rlaalsgh11!'
    }

    response = client.post('/users/signin', json.dumps(user), content_type = 'application/json')

    self.assertEqual(response.json(),{'MESSAGE' : 'INVALID_EMAIL'})
    self.assertEqual(response.status_code, 401)

  def test_signin_failure_invalid_password(self):
    client = Client()

    user = {
      'email'    : 'rlaalsgh@gmail.com',
      'password' : 'rlaalsgh'
    }

    response = client.post('/users/signin', json.dumps(user), content_type = 'application/json')

    self.assertEqual(response.json(),{'MESSAGE' : 'INVALID_PASSWORD'})
    self.assertEqual(response.status_code, 401)

  def test_signin_failure_key_error(self):
    client = Client()

    user = {
      'password' : 'rlaalsgh11!'
    }

    response = client.post('/users/signin', json.dumps(user), content_type = 'application/json')

    self.assertEqual(response.json(),{'MESSAGE' : 'KEY_ERROR'})
    self.assertEqual(response.status_code, 400)