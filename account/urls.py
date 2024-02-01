from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account.views import UserView

app_name = "account"

router = DefaultRouter()

router.register("user", UserView, basename="users")

urlpatterns = [
    path("", include(router.urls)),
]
