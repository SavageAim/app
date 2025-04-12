"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.socialaccount.providers.discord.urls import urlpatterns as discord_urls
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.urls import path, include
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

patterns = [
    path('api/', include(('api.urls', 'api'))),
    path('health/', lambda _: HttpResponse()),
    path('logout/', LogoutView.as_view()),
    path('schema.yaml', SpectacularAPIView.as_view(), name='schema'),
    path('schema/', SpectacularSwaggerView.as_view(url_name='schema'), name='schema-ui'),

    # Auth stuff (TODO - replace this because it's sorta workaroundy)
    path('accounts/', include(discord_urls)),
    # Set auth urls to redirect and display an error message instead
    path(
        'auth/cancelled/',
        RedirectView.as_view(url=f'{settings.LOGIN_REDIRECT_URL}auth/?auth_cancelled=1', permanent=True),
        name='socialaccount_login_cancelled',
    ),
    path(
        'auth/error/',
        RedirectView.as_view(url=f'{settings.LOGIN_REDIRECT_URL}auth/?auth_error=1', permanent=True),
        name='socialaccount_login_error',
    ),
    path(
        'auth/double_email/',
        RedirectView.as_view(url=f'{settings.LOGIN_REDIRECT_URL}auth/?auth_duplicate=1', permanent=True),
        name='socialaccount_signup',
    ),
]

urlpatterns = [
    path('backend/', include(patterns)),
]
