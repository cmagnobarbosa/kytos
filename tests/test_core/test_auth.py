"""Test kytos.core.auth module."""
from unittest import TestCase
from unittest.mock import Mock

import requests
from requests.auth import HTTPBasicAuth

from kytos.core.auth import Auth

API_URI = "http://127.0.0.1:8181/api/kytos/core"


class TestAuth(TestCase):
    """Auth tests."""

    def setUp(self):
        """Instantiate a controller and an Auth."""
        self.controller = Mock()
        self.auth = Auth(self.controller)
        self.token = self.get_token()

    @classmethod
    def get_token(cls):
        """Make a request to get a token to be used in tests"""
        success_response = requests.get(
            "%s/auth/login/" % API_URI, auth=HTTPBasicAuth("test", "test")
        )
        json_response = success_response.json()
        return json_response["token"]

    def validate_schema(self, my_dict, check_against):
        """Check if a dict respects a given schema"""
        for key, value in check_against.items():
            if isinstance(value, dict):
                return self.validate_schema(my_dict[key], value)
            if not isinstance(my_dict[key], value):
                return False
        return True

    def test_01_login_request(self):
        """Test auth login endpoint"""
        success_response = requests.get(
            "%s/auth/login/" % API_URI, auth=HTTPBasicAuth("test", "test")
        )
        error_response = requests.get(
            "%s/auth/login/" % API_URI,
            auth=HTTPBasicAuth("nonexistent", "nonexistent"),
        )

        self.assertEqual(success_response.status_code, 200)
        self.assertEqual(error_response.status_code, 401)

    def test_02_list_users_request(self):
        """Test auth list users endpoint"""
        valid_header = {"Authorization": "Bearer %s" % self.token}
        invalid_header = {"Authorization": "Bearer invalidtoken"}
        schema = {"users": list}
        success_response = requests.get(
            "%s/auth/users/" % API_URI, headers=valid_header
        )
        error_response = requests.get(
            "%s/auth/users/" % API_URI, headers=invalid_header
        )
        is_valid = self.validate_schema(success_response.json(), schema)

        self.assertEqual(success_response.status_code, 200)
        self.assertEqual(error_response.status_code, 401)
        self.assertTrue(is_valid)

    def test_03_create_user_request(self):
        """Test auth create user endpoint"""
        header = {"Authorization": "Bearer %s" % self.token}
        data = {
            "username": "testauth_tempuser",
            "password": "testauth_tempuser",
            "email": "tempuser@kytos.io",
        }
        success_response = requests.post(
            "%s/auth/users/" % API_URI, json=data, headers=header
        )
        error_response = requests.post(
            "%s/auth/users/" % API_URI, json=data, headers=header
        )

        self.assertEqual(success_response.status_code, 200)
        self.assertEqual(error_response.status_code, 409)

    def test_04_list_user_request(self):
        """Test auth list user endpoint"""
        header = {"Authorization": "Bearer %s" % self.token}
        schema = {"data": {"email": str, "username": str}}
        success_response = requests.get(
            "%s/auth/users/%s" % (API_URI, "testauth_tempuser"), headers=header
        )
        error_response = requests.get(
            "%s/auth/users/%s" % (API_URI, "nonexistent"), headers=header
        )
        is_valid = self.validate_schema(success_response.json(), schema)

        self.assertEqual(success_response.status_code, 200)
        self.assertEqual(error_response.status_code, 500)
        self.assertTrue(is_valid)

    def test_05_update_user_request(self):
        """Test auth update user endpoint"""
        header = {"Authorization": "Bearer %s" % self.token}
        data = {"email": "newemail_tempuser@kytos.io"}
        success_response = requests.patch(
            "%s/auth/users/%s" % (API_URI, "testauth_tempuser"),
            json=data,
            headers=header,
        )
        error_response = requests.patch(
            "%s/auth/users/%s" % (API_URI, "nonexistent"),
            json=data,
            headers=header,
        )

        self.assertEqual(success_response.status_code, 200)
        self.assertEqual(error_response.status_code, 500)

    def test_06_delete_user_request(self):
        """Test auth delete user endpoint"""
        header = {"Authorization": "Bearer %s" % self.token}
        success_response = requests.delete(
            "%s/auth/users/%s" % (API_URI, "testauth_tempuser"), headers=header
        )
        error_response = requests.delete(
            "%s/auth/users/%s" % (API_URI, "nonexistent"), headers=header
        )

        self.assertEqual(success_response.status_code, 200)
        self.assertEqual(error_response.status_code, 500)
