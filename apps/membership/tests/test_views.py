from typing import Any

from django.http import HttpRequest, HttpResponseBase
from django.test import TestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.membership.utils import activation_token
from apps.membership.views import ActivateAccountView
from apps.utils import BasicTestsMixin, UserTestsMixin


class ActivateAccountViewTests(BasicTestsMixin, UserTestsMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.request: HttpRequest = self.create_request('/')
        self.inactive_user: Any = self.user_factory(is_active=False)
        self.uidb64: str = urlsafe_base64_encode(force_bytes(self.inactive_user.pk))
        self.invalid_token: str = 'invalid-token'  # noqa S105
        self.correct_token: str = activation_token.make_token(self.inactive_user)

    def test_account_activation_success(self) -> None:
        response: HttpResponseBase = ActivateAccountView.as_view()(
            self.request, uidb64=self.uidb64, token=self.correct_token
        )
        self.inactive_user.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.inactive_user.is_active)

    def test_account_activation_invalid_token(self) -> None:
        response: HttpResponseBase = ActivateAccountView.as_view()(
            self.request, uidb64=self.uidb64, token=self.invalid_token
        )
        self.inactive_user.refresh_from_db()

        self.assertEqual(response.status_code, 400)
        self.assertFalse(self.inactive_user.is_active)

    def test_account_activation_invalid_uidb64(self) -> None:
        invalid_uidb64: str = urlsafe_base64_encode(force_bytes(99999))
        response: HttpResponseBase = ActivateAccountView.as_view()(
            self.request, uidb64=invalid_uidb64, token=self.correct_token
        )

        self.inactive_user.refresh_from_db()

        self.assertEqual(response.status_code, 400)
        self.assertFalse(self.inactive_user.is_active)

    def test_account_activation_user_does_not_exist(self) -> None:
        non_existing_uidb64: str = urlsafe_base64_encode(force_bytes(999999))
        response: HttpResponseBase = ActivateAccountView.as_view()(
            self.request, uidb64=non_existing_uidb64, token=self.correct_token
        )

        self.assertEqual(response.status_code, 400)
