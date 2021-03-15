from django.apps import AppConfig


class CashTransConfig(AppConfig):
    name = 'cash_trans'

    def ready(self):
        import cash_trans.signals
