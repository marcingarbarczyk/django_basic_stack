from django.urls import path

from apps.membership.api_views import (
    ActivateAccountView,
    ChangePasswordView,
    ConfirmResetPasswordView,
    CookieTokenRefreshView,
    DeleteAccountView,
    LoginGoogleView,
    LoginView,
    LogoutView,
    ResetPasswordView,
    UserInfoView,
    UserRegistrationView,
)

urlpatterns = [
    path(
        'user-info/',
        UserInfoView.as_view(),
        name='user-info',
    ),
    path(
        'login/',
        LoginView.as_view(),
        name='login',
    ),
    path(
        'login-google/',
        LoginGoogleView.as_view(),
        name='login-google',
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout',
    ),
    path(
        'refresh/',
        CookieTokenRefreshView.as_view(),
        name='token-refresh',
    ),
    path(
        'register/',
        UserRegistrationView.as_view(),
        name='register',
    ),
    path(
        'activate/<str:uidb64>/<str:token>/',
        ActivateAccountView.as_view(),
        name='activate',
    ),
    path(
        'delete-account/',
        DeleteAccountView.as_view(),
        name='delete-account',
    ),
    path(
        'change-password/',
        ChangePasswordView.as_view(),
        name='change-password',
    ),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('confirm-reset-password/', ConfirmResetPasswordView.as_view(), name='confirm-reset-password'),
]
