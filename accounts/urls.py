from django.urls import path
from .views import RegisterView, LoginView, ProfileView, google_login

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path("profile/", ProfileView.as_view(), name="profile"),
    path('google-login/', google_login, name='google-login'),
]
