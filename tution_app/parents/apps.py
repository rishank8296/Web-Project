from django.apps import AppConfig

class ParentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tution_app.parents'

    def ready(self):
        import tution_app.parents.signals
