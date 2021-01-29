from .temp_views import daru_spin
from django.urls import path


app_name = 'daru_wheel'

urlpatterns = [
    path('', daru_spin, name="daru_spin"),
]
