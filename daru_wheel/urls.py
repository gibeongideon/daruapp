from .import temp_views as views
from django.urls import path


app_name = 'daru_wheel'

urlpatterns = [
    path('', views.daru_spin, name="daru_spin"),
    path('ispin', views.i_spin, name="i_spin"),
]
