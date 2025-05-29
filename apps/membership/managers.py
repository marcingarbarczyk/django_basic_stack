from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email=email, password=password, **extra_fields)

    def get_active_users(self):
        """
        Returns a queryset of all active users.
        """
        return self.filter(is_active=True)

    def get_inactive_users(self):
        """
        Returns a queryset of all inactive users.
        """
        return self.filter(is_active=False)
