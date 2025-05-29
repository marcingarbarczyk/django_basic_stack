from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext as _
from django.views.generic import FormView

from apps.membership.forms import UserLoginForm, UserRegisterForm
from apps.membership.utils import activation_token


class LoginFormView(LoginView):
    """
    Login form view for user authentication.
    """

    form_class = UserLoginForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form


class RegisterFormView(FormView):
    """
    Registration form view for creating a new user account and sending an activation email.
    """

    template_name = 'membership/register_form.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        """
        Called when the submitted form is valid. Saves the user and sends an activation email.
        """
        user = form.save()
        self.send_activation_email(user)
        messages.success(self.request, _('Account created. An activation link has been sent to your email address.'))
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Called when the submitted form is invalid.
        """
        messages.error(self.request, _('An error occurred. Please try again.'))
        return super().form_invalid(form)

    def send_activation_email(self, user):
        """
        Sends an account activation email to the new user.
        """
        token = activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = self.request.build_absolute_uri(
            reverse_lazy('activate', kwargs={'uidb64': uid, 'token': token})
        )
        subject = _('Activate Your Account')
        message = render_to_string(
            'membership/email/activation_email.html',
            {
                'user': user,
                'activation_link': activation_link,
            },
        )
        plain_message = strip_tags(message)
        send_mail(subject, plain_message, 'youremail@example.com', [user.email], html_message=message)
