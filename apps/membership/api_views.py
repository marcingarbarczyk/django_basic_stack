from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext as _
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from apps.membership.serializers import CustomUserSerializer, LoginUserSerializer, RegisterUserSerializer
from apps.membership.throttling import LoginRateThrottle, RegisterRateThrottle
from apps.membership.utils import activation_token

User = get_user_model()


class LoginView(APIView):
    """
    API view for handling user login and token generation.
    """

    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Authenticates the user and provides access and refresh tokens along with expiry dates.
        """
        serializer = LoginUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)

            access_token = str(refresh.access_token)
            access_token_expiry = refresh.access_token['exp']

            refresh_token = str(refresh)
            refresh_token_expiry = refresh['exp']

            # Response payload
            response_data = {
                'user': CustomUserSerializer(user).data,
                'access_token_expiry': access_token_expiry,
                'refresh_token_expiry': refresh_token_expiry,
            }

            response = Response(response_data, status=status.HTTP_200_OK)
            response.set_cookie(key='access_token', value=access_token, httponly=True, secure=True, samesite='None')
            response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, secure=True, samesite='None')
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginGoogleView(APIView):
    """
    API view for handling user login with Google and providing JWT tokens.
    Only allows existing users to log in.
    """

    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]

    def post(self, request, *args, **kwargs):
        """
        Authenticates the user via Google and provides JWT tokens if the user exists.
        """
        # Google token sent from the front-end
        google_token = request.data.get('token')

        # Validate presence of token
        if not google_token:
            return Response({'error': 'Token is required.'}, status=400)

        try:
            # Verify the Google ID token
            google_user_info = id_token.verify_oauth2_token(google_token, google_requests.Request())

            # Extract user's email from the token payload
            email = google_user_info.get('email')

            # Check if a user with the given email exists in the database
            try:
                user = User.objects.get(email=email)

                # Generate JWT tokens for the user
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    },
                    status=200,
                )

            except User.DoesNotExist:
                # User does not exist
                return Response(
                    {'error': 'User with this email does not exist. Please contact support.'},
                    status=404,
                )

        except ValueError:
            # Token verification failed
            return Response({'error': 'Invalid token.'}, status=400)


class LogoutView(APIView):
    """
    API view for handling user logout and token invalidation.
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Invalidates the refresh token and deletes authentication cookies.
        """
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()
            except InvalidToken:
                pass

            except Exception as e:
                return Response(
                    {'error': _('Error during token invalidation: ') + str(e)}, status=status.HTTP_400_BAD_REQUEST
                )

        response = Response({'message': _('Successfully logged out!')}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response


class CookieTokenRefreshView(TokenRefreshView):
    """
    API view for refreshing the access token using the refresh token stored in cookies.
    Also returns expiration times for both tokens.
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Retrieves the refresh token from cookies, issues a new access token,
        and includes token expiry times in the response.
        """
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'error': _('Refresh token not provided')}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            if refresh.is_expired:
                raise TokenError('Refresh token has expired')
            access_token = str(refresh.access_token)
            access_token_expiry = refresh.access_token['exp']
            refresh_token_expiry = refresh['exp']

            response_data = {
                'message': _('Access token refreshed successfully'),
                'access_token_expiry': access_token_expiry,
                'refresh_token_expiry': refresh_token_expiry,
            }

            response = Response(response_data, status=status.HTTP_200_OK)
            response.set_cookie(key='access_token', value=access_token, httponly=True, secure=True, samesite='None')
            return response
        except InvalidToken:
            return Response({'error': _('Invalid token')}, status=status.HTTP_401_UNAUTHORIZED)


class UserRegistrationView(CreateAPIView):
    """
    API View for user registration with account activation email.
    """

    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]
    throttle_classes = [RegisterRateThrottle]

    def perform_create(self, serializer):
        """
        Handles user creation and sends an activation email.
        """
        user = serializer.save()
        self.send_activation_email(user)

    def send_activation_email(self, user):
        """
        Sends an account activation email to the new user.
        """
        token = activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        frontend_base_url = 'http://localhost:5173/activate'
        activation_link = f'{frontend_base_url}?uidb64={uid}&token={token}'
        subject = 'Activate Your Account'
        message = render_to_string(
            'membership/email/activation_email.html',
            {
                'user': user,
                'activation_link': activation_link,
            },
        )
        plain_message = strip_tags(message)
        send_mail(subject, plain_message, 'youremail@example.com', [user.email], html_message=message)

    def create(self, request, *args, **kwargs):
        """
        Overrides the default create method to customize the response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'detail': 'Account created. An activation link has been sent to your email address.'},
            status=status.HTTP_201_CREATED,
        )


class UserInfoView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        password = request.data.get('password')
        if not password or not authenticate(email=user.email, password=password):
            return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

        # Perform deletion
        user.delete()

        return Response({'message': 'Account deleted successfully.'}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not user.check_password(current_password):
            return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the new password
        try:
            validate_password(new_password, user=user)
        except DjangoValidationError as e:
            # Collect all validation error messages
            errors = [error for error in e.messages]  # noqa
            raise ValidationError({'errors': errors})

        # Set the new password
        user.set_password(new_password)
        user.save()

        # Optionally update the last login timestamp
        update_last_login(None, user)

        # Return success response
        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)


class ActivateAccountView(APIView):
    """
    API view to activate a user's account with deactivation date check.
    """

    permission_classes = [AllowAny]

    def get(self, request, uidb64, token, *args, **kwargs):
        """
        Activates the account if the token is valid, the user is inactive, and has not been deactivated after token issuance.
        """
        try:
            # Decode the user ID
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise NotFound('Invalid user or user does not exist.')

        # Check if the user is already active
        if user.is_active:
            return Response({'error': 'Account is already active.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user was deactivated
        if user.deactivation_date:
            return Response(
                {'error': 'Your account has been deactivated. Please contact support for reactivation.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Verify the token
        if activation_token.check_token(user, token):
            # Activate the user account if token is valid
            user.is_active = True
            user.save()
            return Response({'message': 'Account activated successfully!'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """
    API endpoint to request a password reset email.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'message': 'If the email exists, a password reset link will be sent.'}, status=status.HTTP_200_OK
            )

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://localhost:5173/confirm-reset-password?uidb64={uid}&token={token}"

        # Send password reset email
        subject = 'Reset Your Password'
        message = f"Click the link below to reset your password:\n{reset_link}"
        send_mail(subject, message, 'noreply@example.com', [user.email])

        return Response(
            {'message': 'If the email exists, a password reset link will be sent.'}, status=status.HTTP_200_OK
        )


class ConfirmResetPasswordView(APIView):
    """
    API endpoint to reset the password using the UID and token.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        uidb64 = request.data.get('uidb64')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        if not uidb64 or not token or not new_password:
            return Response({'error': 'UID, token, and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid UID or token.'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid token or token has expired.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password has been successfully reset.'}, status=status.HTTP_200_OK)
