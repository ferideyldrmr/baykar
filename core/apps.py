from django.apps import AppConfig
from django.contrib.auth import authenticate


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'


class AuthenticateConfig(AppConfig):
    name = 'authenticate'
