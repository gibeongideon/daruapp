from .import temp_views as views
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import api_view

router = DefaultRouter()
router.register(r'', api_view.StakeViewSet,basename='Stake')


app_name = 'daru_wheel'

urlpatterns = [
    path('stake', include(router.urls)),

    path('', views.spin, name="spin"),
    path('spin_it', views.spin_it, name="spin_it"),

    path('spin', views.daru_spin, name="daru_spin"),
  
]
