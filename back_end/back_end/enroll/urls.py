from django.urls import path
from .views import UserRegisterView, home, UserLoginView

urlpatterns = [
    path('user/register/',UserRegisterView.as_view(),name='user-register'),
    path('user/login/', UserLoginView.as_view(), name='user-login'),

    path('', home, name='home'),
]
