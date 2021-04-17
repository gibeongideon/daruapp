from .views import mpesa_deposit
from django.urls import path


app_name = 'cash_trans'


urlpatterns = [
    path('mpesa_deposit/', mpesa_deposit, name="mpesa_deposit"),
    # path('sign_up/', sign_up, name="sign_up"),
    # path('register/', register_user, name="register_user"),
    # path('log_out/', log_out, name="log_out"),
    # path('', daru_spin, name="daru_spin"),
    # path('user_list/', user_list, name="user_list"),
    # path("logout/", LogoutView.as_view(), name="logout")

]
