from django.apps import AppConfig

class GamerzConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gamerz'

    def ready(self):
        import gamerz.signals