from django.apps import AppConfig


class ConstructionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'construction'

    def ready(self):
        import construction.signals