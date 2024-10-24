# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import create_user,change_password,update_user_info,get_users_all,delete_users,get_users_one

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create_user/', create_user, name='create_user'),
    path('change_password/', change_password, name='change_password'),
    path('update_user_info/', update_user_info, name='update_user_info'),
    path('getall/', get_users_all, name='get_users_all'),
    path('getuser/', get_users_one, name='get_users_one'),
    path('delete_user/', delete_users, name='delete_user'),
]
