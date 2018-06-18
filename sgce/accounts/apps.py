from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'sgce.accounts'

    def ready(self):
        import sgce.accounts.signals