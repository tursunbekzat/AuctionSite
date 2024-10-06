# auth/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # path('register/', RegistrationView.as_view(), name='register'),
    # path('login/', LoginView.as_view(), name='login'),
    # path('user/', UserView.as_view(), name='user'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
]
