from django.apps import AppConfig


class DaruWheelConfig(AppConfig):
    name = 'daru_wheel'
    
    def ready(self):
        import daru_wheel.signals