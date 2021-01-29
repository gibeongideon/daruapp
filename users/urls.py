from .api_views import UserRecordView
from rest_framework.routers import DefaultRouter

from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from . import template_views as views
from django.urls import reverse_lazy

router = DefaultRouter()

app_name = 'users'

urlpatterns = [
    # path('', include(router.urls)),
    path('user/', UserRecordView.as_view(), name='users'),

    path('user_page', views.user_page, name="user_page"),
    path('notification', views.notification, name="notification"),
    path('mine_users/', views.mine_users, name="mine_users"),

    path('login', views.CustomLoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('register', views.register, name='register'),

    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='password/password_change.html'),
        name='password_change'),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='password/password_change_done.html'),
        name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password/password_reset_form.html',
        email_template_name='password/password_reset_email.html',
        subject_template_name='password/password_reset_subject.txt',
        success_url=reverse_lazy('users:password_reset_done'),      
        ), name='password_reset'),

    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(
        template_name='password/password_reset_done.html'),
        name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password/password_reset_confirm.html',
        success_url=reverse_lazy('users:password_reset_complete')),
        name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password/password_reset_complete.html'),
        name='password_reset_complete'),
]


