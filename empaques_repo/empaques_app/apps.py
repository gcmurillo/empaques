from django.apps import AppConfig
from django.db.models.signals import post_save
from .models import OrdenEmpaquesDetail

class CilindroAppConfig(AppConfig):
    name = 'empaques_app'

    def ready(self):
        from .signals import *
