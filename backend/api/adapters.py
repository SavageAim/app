from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from sentry_sdk import capture_exception


class SavageAimAccountAdapter(DefaultSocialAccountAdapter):

    def authentication_error(self, request, provider_id, error=None, exception=None, extra_context=None):
        if exception is not None:
            capture_exception(exception)
        raise ImmediateHttpResponse(redirect(reverse('socialaccount_login_error')))
