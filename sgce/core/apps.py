from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'sgce.core'

    def ready(self):
        import sgce.core.signals