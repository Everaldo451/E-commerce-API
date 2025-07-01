from .views import LoginView, LogoutView, RefreshView
from django.urls import path

urlpatterns = [
    path("login/", LoginView.as_view(), name='auth-login'),
    path("logout/", LogoutView.as_view(), name='auth-logout'),
    path("refresh/", RefreshView.as_view(), name='auth-refresh')
]
