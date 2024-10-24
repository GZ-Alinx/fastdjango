from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('create/', views.create_job, name='create_job'),
    path('show/', views.select_job_one, name='select_job_one'),
    path('showall/', views.select_job_all, name='select_job_all'),
    path('delete/', views.delete_job, name='delete_job'),
    path('stop/', views.stop_job, name='stop_job'),
    path('start/', views.run_job, name='run_job')
]

