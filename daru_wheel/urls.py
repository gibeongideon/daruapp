from .temp_views import daru_spin, i_spin
from django.urls import path


app_name = 'daru_wheel'

urlpatterns = [
    path('', daru_spin, name="daru_spin"),
    path('ispin', i_spin, name="i_spin"),
]
