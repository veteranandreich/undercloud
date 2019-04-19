from django.test import TestCase
from accounts.models import User
from profiles.models import Profile
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
        self.client = APIClient()
        response = self.client.post('/api/register', {
            "username":"pelevin",
            "email": "test_user1@example.com",
            "password": "secret"
        }, format="json")
        u = User.objects.last()
        u.is_active = True
        u.save()
        response = self.client.post('/api/jwt-auth/', {
            "username":"pelevin",
            "password": "secret"
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

        user = User.objects.last()
        user.is_active = True
        user.save()
        profile = Profile(owner = user)
        profile.save()
        self.user = user

        response = self.client.post('/api/jwt-auth/', {
            "username":"pelevin",
            "password": "secret"
        })
        token = response.json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def test_profile_post_api(self):
        response = self.client.post("/api/profiles")
        self.assertTrue(response.status_code == 200)

    def test_profile_get_api(self):
        response = self.client.get("/api/profiles")
        self.assertTrue(response.status_code == 200)

    def test_profile_HEAD_api(self):
        response = self.client.head("/api/profiles")
        self.assertTrue(response.status_code == 200)

    def test_profilepk_api(self):
        response = self.client.get("/api/profiles/"+str(self.user.pk))
        self.assertTrue(response.status_code==200)

    def test_profile_patch_api(self):
        response = self.client.get("/api/profiles/"+str(self.user.pk))
        response = self.client.patch("/api/profiles/"+str(self.user.pk),{"status":"teststatus"})
        self.assertTrue(response.json()["status"]!="")