from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from django.utils.translation import gettext as _
from geoip2.errors import AddressNotFoundError
from ipware.ip import get_client_ip

try:
    from django.contrib.gis.geoip2 import GeoIP2, GeoIP2Exception

    geo_ip = GeoIP2()
except GeoIP2Exception:

    class FakeGeoIP2:
        @staticmethod
        def city(*args, **kwargs):
            return {'errors': ['GeoIP2Exception']}

    if not settings.DEBUG:
        raise

    geo_ip = FakeGeoIP2()


def get_geo_data(ip=None):
    """
    Retrieves geolocation data based on an IP address.

    Args:
        ip (str, optional): The IP address for which geolocation data is fetched.

    Returns:
        dict: Geolocation data or error information if retrieval fails.
    """
    if ip is None:
        return {}
    try:
        data = geo_ip.city(ip)
    except AddressNotFoundError:
        data = {'errors': [_('Address not found.')]}
    return data


def get_device_info(request):
    """
    Retrieves information about the user's device.

    Args:
        request (HttpRequest): HTTP request object.

    Returns:
        dict: Information about the operating system and browser of the user's device.
    """
    return {
        'os': {'family': request.user_agent.os[0], 'os_version': request.user_agent.os[2]},
        'browser': {'family': request.user_agent.browser[0], 'browser_version': request.user_agent.browser[2]},
    }


def handle_login_attempt(request, username):
    """
    Handles login attempts and locks out a user after too many failed attempts.

    Args:
        request (HttpRequest): HTTP request object.
        username (str): Username of the person attempting to log in.

    Raises:
        TooManyLoginAttemptsException: If the user exceeds the maximum allowed login attempts.

    Returns:
        LoginAttempt: The created LoginAttempt object.
    """
    from .exceptions import TooManyLoginAttemptsException
    from .models import LoginAttempt

    ip, _ = get_client_ip(request)
    attempts_count = LoginAttempt.objects.filter(
        ip=ip,
        has_logged_in=False,
        attempted_at__gte=timezone.now() - timezone.timedelta(minutes=settings.LOGIN_ATTEMPTS_TIMEOUT_MINUTES),
    ).count()

    if attempts_count >= settings.MAX_LOGIN_ATTEMPTS:
        raise TooManyLoginAttemptsException

    login_attempt = LoginAttempt.objects.create(
        username=username,
        ip=ip,
        user=None,
        browser=get_device_info(request),
        attempted_at=timezone.now(),
        geolocation=get_geo_data(ip),
        has_logged_in=False,
    )

    return login_attempt


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Token generator for account activation.
    """

    def _make_hash_value(self, user, timestamp):
        """
        Generates the hash value for the token.

        Args:
            user (User): User for whom the token is generated.
            timestamp (int): The timestamp of token generation.

        Returns:
            str: The hash value for the token.
        """
        return f"{user.pk}{timestamp}{user.is_active}"


activation_token = AccountActivationTokenGenerator()
