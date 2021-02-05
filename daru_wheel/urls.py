from .import temp_views as views
from django.urls import path


app_name = 'daru_wheel'

urlpatterns = [

    path('', views.spin, name="spin"),
    path('spin', views.daru_spin, name="daru_spin"),
    
    
]
