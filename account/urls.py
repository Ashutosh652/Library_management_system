from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account.views import UserView, LoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt

app_name = "account"

router = DefaultRouter()

router.register("user", UserView, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
