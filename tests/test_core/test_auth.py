"""Test kytos.core.auth module."""
import requests
from requests.auth import HTTPBasicAuth
from unittest import TestCase
from unittest.mock import Mock

from kytos.core.auth import Auth

API_URI = "http://127.0.0.1:8181/api/kytos/core"

class TestAuth(TestCase):
    """Auth tests."""

    def setUp(self):
        """Instant a controller"""
        self.controller = Mock()
        self.auth = Auth(self.controller)
        self.token = self.get_token()

    def get_token(self):
        success_response = requests.get("%s/auth/login/" % API_URI,
                        auth=HTTPBasicAuth("test", "test"))
        json_response = success_response.json()
        return json_response["token"]

    def test_01_login_request(self): 
        success_response = requests.get("%s/auth/login/" % API_URI,
                                auth=HTTPBasicAuth("test", "test"))
        error_response = requests.get("%s/auth/login/" % API_URI,
                                auth=HTTPBasicAuth("nonexistent", "nonexistent"))
        self.assertEqual(success_response.status_code, 200)
        # self.assertEqual(error_response.status_code, 401)

    def test_02_list_users_request(self):
        header = {"Authorization": "Bearer %s" % self.token}
        success_response = requests.get("%s/auth/users/" % API_URI,
                                        headers=header)
        # print(success_response.json())
        self.assertEqual(success_response.status_code, 200)

    def test_03_list_user_request(self):
        header = {"Authorization": "Bearer %s" % self.token}
        success_response = requests.get("%s/auth/users/%s" % (API_URI, "test"),
                                        headers=header)
        # print(success_response.json())
        self.assertEqual(success_response.status_code, 200)

    def test_04_create_user_request(self):
        header = {"Authorization": "Bearer %s" % self.token}
        data = {
            "username": "testauth_tempuser",
            "password": "testauth_tempuser",
            "email": "tempuser@kytos.io"
        }
        success_response = requests.post("%s/auth/users/" % API_URI,
                                        json=data, headers=header)
        error_response = requests.post("%s/auth/users/" % API_URI,
                                        json=data, headers=header)
        self.assertEqual(success_response.status_code, 200)
        self.assertEqual(error_response.status_code, 409)

    def test_05_update_user_request(self):
        header = {"Authorization": "Bearer %s" % self.token}
        data = {
            "email": "newemail_tempuser@kytos.io"
        }
        success_response = requests.patch("%s/auth/users/%s" % (API_URI, "testauth_tempuser"),
                                        json=data, headers=header)
        error_response = requests.patch("%s/auth/users/%s" % (API_URI, "nonexistent"),
                                        json=data, headers=header)
        self.assertEqual(success_response.status_code, 200)
        self.assertEqual(error_response.status_code, 500)

    def test_06_delete_user_request(self):
        header = {"Authorization": "Bearer %s" % self.token}
        success_response = requests.delete("%s/auth/users/%s" % (API_URI, "testauth_tempuser"),
                                           headers=header)
        error_response = requests.delete("%s/auth/users/%s" % (API_URI, "nonexistent"),
                                         headers=header)
        self.assertEqual(success_response.status_code, 200)
        self.assertEqual(error_response.status_code, 500)
