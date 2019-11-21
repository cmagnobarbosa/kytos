"""Test kytos.core.auth module."""
import getpass
from unittest import TestCase
from unittest.mock import Mock, patch
from kytos.core.auth import Auth


def input_password():
    """Get password value"""
    password = getpass.getpass()
    return password


def input_value():
    """Get input value"""
    value = input()
    return value


class TestAuth(TestCase):
    """Auth tests."""

    def setUp(self):
        """Instant a controller"""
        self.controller = Mock()
        self.auth = Auth(self.controller)
        self.auth._find_user(12)

    def tearDown(self):
        """TearDown"""


    @patch("controller.buffers.app.put")
    def test_buffer(self, buffer_mock):
        response = {"answer": "mock test", "code": 201}
        buffer_mock.__get_item__.return_value = response
        self.assertEqual(True, True)

    @classmethod
    @patch("getpass.getpass")
    def test_getpass(cls, password):
        """Test when getpass is calling on authentication."""
        password.return_value = "youshallnotpass"
        assert input_password() == password.return_value

    @classmethod
    @patch("builtins.input")
    def test_user_values(cls, user_value):
        """Test when input is calling on authentication."""
        user_value.return_value = "kuser"
        assert input_value() == user_value.return_value
