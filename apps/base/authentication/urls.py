from django.urls import path
from .views import home, login, check_status_login, success

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('check_status_login/', check_status_login, name='check_status_login'),
    path('success/', success, name='success'),
]