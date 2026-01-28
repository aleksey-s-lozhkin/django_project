from django.contrib.auth.views import LogoutView
from .views import RegisterView, CustomLoginView
from django.urls import path
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(
        next_page='catalog:home'
    ), name='logout'),
]

