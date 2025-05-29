from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext as _

from apps.membership.managers import UserManager
from apps.utils.models import ActiveMixin, TimeStampMixin


class User(AbstractBaseUser, PermissionsMixin, TimeStampMixin, ActiveMixin):
    """
    A user model using email as the username.
    """

    email = models.EmailField(
        unique=True,
        verbose_name=_('e-mail'),
    )
    first_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name=_('first name'),
    )
    last_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name=_('last name'),
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('staff status'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class LoginAttempt(TimeStampMixin):
    """
    A model representing a user's login attempt.
    """

    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('user'),
    )
    username = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('username'),
    )
    attempted_at = models.DateTimeField(
        verbose_name=_('attempt date and time'),
    )
    has_logged_in = models.BooleanField(
        blank=True,
        default=False,
        verbose_name=_('logged in'),
    )
    browser = models.CharField(
        max_length=300,
        blank=True,
        verbose_name=_('browser'),
    )
    ip = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name=_('IP address'),
    )
    geolocation = JSONField(
        default={},
        blank=True,
        verbose_name=_('geolocation'),
    )

    @property
    def city(self):
        return self.geolocation.get('city', '')

    def __str__(self):
        return _('Login attempt by {username}').format(username=self.username)

    class Meta:
        verbose_name = _('user login attempt')
        verbose_name_plural = _('user login attempts')
