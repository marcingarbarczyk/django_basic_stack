from django.test import TestCase

from apps.membership.models import User
from apps.utils import UserTestsMixin


class UserManagerTests(UserTestsMixin, TestCase):
    def test_get_active_users(self):
        active_user_1 = self.user_factory.create()
        active_user_2 = self.user_factory.create()
        inactive_user = self.user_factory.create(
            is_active=False,
        )

        active_users = User.objects.get_active_users()
        self.assertIn(active_user_1, active_users)
        self.assertIn(active_user_2, active_users)
        self.assertNotIn(inactive_user, active_users)

    def test_get_inactive_users(self):
        active_user = self.user_factory.create()
        inactive_user_1 = self.user_factory.create(
            is_active=False,
        )
        inactive_user_2 = self.user_factory.create(
            is_active=False,
        )

        inactive_users = User.objects.get_inactive_users()
        self.assertIn(inactive_user_1, inactive_users)
        self.assertIn(inactive_user_2, inactive_users)
        self.assertNotIn(active_user, inactive_users)
