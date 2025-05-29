from typing import Any, Optional

from django import forms
from django.conf import settings
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpRequest
from django.utils.translation import gettext as _

from apps.membership.exceptions import TooManyLoginAttemptsException
from apps.membership.models import User
from apps.membership.utils import handle_login_attempt


class BaseLoginForm(forms.Form):
    """
    Base form used for authentication forms.
    """

    request: Optional[HttpRequest] = None

    def _handle_login_attempt(self, username: Optional[str]) -> Any:
        """
        Helper method to process login attempts, including exception handling.
        """
        try:
            if self.request is None:
                raise ValueError(_('Request object is not set.'))
            login_attempt = handle_login_attempt(self.request, username)
        except TooManyLoginAttemptsException:
            raise forms.ValidationError(
                _('Login attempt limit exceeded. Please try again in {} minutes.').format(
                    settings.LOGIN_ATTEMPTS_TIMEOUT_MINUTES
                ),
                code='too_many_attempts',
            )
        return login_attempt


class AdminLoginForm(AdminAuthenticationForm, BaseLoginForm):
    """
    Custom admin login form.
    """

    def clean(self) -> dict[str, Any]:
        cleaned_username: Optional[str] = self.cleaned_data.get('username')
        login_attempt = self._handle_login_attempt(cleaned_username)

        validated_data = super().clean()
        login_attempt.has_logged_in = True
        login_attempt.user = self.user_cache
        login_attempt.save()
        return validated_data


class UserLoginForm(AuthenticationForm, BaseLoginForm):
    """
    Custom user login form (non-staff).
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.request: Optional[HttpRequest] = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def confirm_login_allowed(self, user: User) -> None:
        if not user.is_active:
            raise forms.ValidationError(
                _('This account is inactive.'),
                code='inactive',
            )

    def clean(self) -> dict[str, Any]:
        cleaned_username: Optional[str] = self.cleaned_data.get('username')
        login_attempt = self._handle_login_attempt(cleaned_username)

        validated_data = super().clean()
        login_attempt.has_logged_in = True
        login_attempt.user = self.user_cache
        login_attempt.save()
        return validated_data


class UserRegisterForm(UserCreationForm):
    """
    Custom user registration form.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = True
        self.fields['password2'].required = True

    email = forms.EmailField(
        required=True,
    )

    class Meta:
        model = User
        fields = [
            'email',
            'password1',
            'password2',
        ]

    def save(self, commit: bool = True) -> User:
        user: User = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False
        if commit:
            user.save()
        return user
