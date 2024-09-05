from django.apps import AppConfig
"""Приложение для управления статичными страницами"""


class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
