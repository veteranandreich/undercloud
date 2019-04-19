from django.test import TestCase
from accounts.models import User
import json
import requests

from rest_framework.test import APIClient


class ApiViewTest(TestCase):

    def test_register_api(self):
        self.client = APIClient()
        response = self.client.post('/api/register', {
            "username":"pelevin",
            "email": "test_user1@example.com",
            "password": "secret"
        }, format="json")
        self.assertEqual(response.status_code, 201)

    def test_registered_user_api(self):
        self.client = APIClient()
        response = self.client.post('/api/register', {
            "username":"pelevin",
            "email": "test_user1@example.com",
            "password": "secret"
        }, format="json")
        self.assertEqual("pelevin",str(User.objects.last()))

    def test_auth_api(self):
        response = requests.post('http://127.0.0.1:8000/api/jwt-auth/', {
            "username":"Pelevin",
            "password": "qwerty"
        })
        self.assertTrue(response.json()["token"])
class AuthApiViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        response = self.client.post('/api/register', {
            "username": "pelevin",
            "email": "test_user1@example.com",
            "password": "secret"
        }, format="json")
        response = requests.post('http://127.0.0.1:8000/api/jwt-auth/', {
            "username":"admin",
            "password": "admin"
        })
        token = response.json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def test_profile_post_api(self):
        response = requests.post('http://127.0.0.1:8000/api/jwt-auth/', {
            "username":"admin",
            "password": "admin"
        })
        token = response.json()["token"]
        value_header = 'JWT ' + token
        response = requests.post("http://127.0.0.1:8000/api/profiles", headers={"Authorization":value_header})
        self.assertTrue(response.status_code == 200)

    def test_profile_get_api(self):
        response = requests.post('http://127.0.0.1:8000/api/jwt-auth/', {
            "username":"admin",
            "password": "admin"
        })
        token = response.json()["token"]
        value_header = 'JWT ' + token
        response = requests.get("http://127.0.0.1:8000/api/profiles", headers={"Authorization":value_header})
        self.assertTrue(response.status_code == 200)

    def test_profile_HEAD_api(self):
        response = requests.post('http://127.0.0.1:8000/api/jwt-auth/', {
            "username":"admin",
            "password": "admin"
        })
        token = response.json()["token"]
        value_header = 'JWT ' + token
        response = requests.head("http://127.0.0.1:8000/api/profiles", headers={"Authorization":value_header})
        self.assertTrue(response.status_code == 200)

    def test_profilepk_api(self):
        response = requests.post('http://127.0.0.1:8000/api/jwt-auth/', {
            "username":"admin",
            "password": "admin"
        })
        token = response.json()["token"]
        value_header = 'JWT ' + token
        response = requests.get("http://127.0.0.1:8000/api/profiles/4", headers={"Authorization":value_header})
        self.assertTrue(response.status_code==200)