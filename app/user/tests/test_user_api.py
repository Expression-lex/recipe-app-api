from django.forms.fields import EmailField
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def craete_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_vaild_user_success(self):
        """Test creating user with vaild payload is successful"""
        payload = {
            'email' : 'alex@yahoo.com',
            'password': 'testpass',
            'name': 'Test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

        def test_user_exists(self):
            """Test creating a user that already exists fails"""
            payload = {
            'email' : 'alex@yahoo.com',
            'password': 'testpass',
            'name': 'Test name'
            }
            craete_user(**payload)
             
            res =self.client.post(CREATE_USER_URL, payload)

            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def test_password_too_short(self):
            """Test taht the password must be more than 5 characters"""
            payload = {'email': 'alex@yahoo.com', 'password': 'pw', 'name':'anlex'}
            res = self.client.post(CREATE_USER_URL, payload)

            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQEUST)
            user_exists = get_user_model().objects.filter(
                email=payload('email')
            ).exists()
            self.assertFalse(user_exists)
         
        def test_create_token_for_user(self):
            """Test that a token is craeted for the user"""
            payload = {'email': 'alex@yahoo.com', 'password': 'password'}
            craete_user(**payload)
            res = self.client.post(TOKEN_URL, payload)

            self.assertIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_200_OK)

        def test_create_token_invaild_credentials(self):
            """Test token if invalid or not"""
            payload = {'email': 'alex@yahoo.com', 'password': 'wrong'}
            craete_user(email='alex@yahoo.com', password="password")
            res = self.client.post(TOKEN_URL, payload)

            self.assertNotIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def test_create_token_no_user(self):
            """Test that token is not created if user doesnt exist"""
            payload = {'email': 'alex@yahoo.com', 'password': 'password'}
            res = self.client.post(TOKEN_URL, payload)

            self.assertNotIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def test_create_token_missing_field(self):
            """Test that email and password are required"""
            res = self.client.post(TOKEN_URL, {'email': 'one', 'password':''})
            self.assertNoIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)