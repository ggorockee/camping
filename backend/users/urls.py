from django.urls import re_path, path
from . import views


urlpatterns = [
    path("register/", views.UserRegistrationView.as_view(), name="user_register"),
    path("token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", views.MyTokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("me/", views.MyInfoView.as_view(), name="my_info"),
]
