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
from allauth.socialaccount.views import login_cancelled, login_error
from django.contrib.auth.views import LogoutView
from django.urls import path, include

patterns = [
    path('api/', include(('api.urls', 'api'))),

    # Auth stuff (TODO - replace this because it's sorta workaroundy)
    path('accounts/', include(discord_urls)),
    path('auth/cancelled/', login_cancelled, name='socialaccount_login_cancelled'),
    path('auth/error/', login_error, name='socialaccount_login_error'),
    path('logout/', LogoutView.as_view()),
]

urlpatterns = [
    path('backend/', include(patterns)),
]
