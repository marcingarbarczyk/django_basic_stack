from apz_toolkit.membership.tests.factories import StaffUserFactory, UserFactory
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory


class BasicTestsMixin:
    """
    Mixin z podstawowymi konfiguracjami dla testów
    """

    request_factory = RequestFactory()
    session_middleware = SessionMiddleware(lambda x: x)
    message_middleware = MessageMiddleware(lambda x: x)

    def create_request(self, path):
        request = self.request_factory.get(path)
        self.session_middleware.process_request(request)
        self.message_middleware.process_request(request)
        return request


class UserTestsMixin:
    """
    Mixin dostarczający fabryki do tworzenia użytkowników + dwóch użytkowników wygenerowanych
    """

    user_factory = UserFactory
    staff_user_factory = StaffUserFactory

    def setUp(self) -> None:
        super().setUp()
        self.user = self.user_factory()
        self.staff_user = self.staff_user_factory()
