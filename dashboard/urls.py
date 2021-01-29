

from django.urls import path, re_path
from dashboard import views
# from daruwheel import views as spinview

app_name = 'dashboard'

urlpatterns = [
    # Matches any html file 
    re_path(r'^.*\.html', views.pages, name='pages'),

    # The home page
    path('', views.index, name='index'),
    path('icons', views.icons, name='icons'),
    path('maps', views.maps, name='maps'),
    path('topo', views.topo, name='topo'),
    path('support', views.support, name='support'),

]
