"""User test."""
from django.test import TestCase

from apps.account.models import User


class UserTestCase(TestCase):
    def setUp(self):
        """Method called to prepare the test."""
        User.objects.create_user(
            email="user@example.com",
            password="123456789",
        )
        User.objects.create_superuser(
            email="admin@example.com",
            password="123456789",
        )

    def test_create_user(self):
        """Validate the creation of a user."""
        user = User.objects.get(email="user@example.com")
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_superuser, False)

    def test_create_superuser(self):
        """Validate the creation of a super user"""
        super_user = User.objects.get(email="admin@example.com")
        self.assertEqual(super_user.is_staff, True)
        self.assertEqual(super_user.is_active, True)
        self.assertEqual(super_user.is_superuser, True)
