from django.contrib.auth.forms import  AuthenticationForm
from django.utils.translation import gettext, gettext_lazy as _


class AuthForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
                'Invalid login credentials. Please check your username and password and try again'
        ),
        'inactive': _("This account is inactive."),
    }