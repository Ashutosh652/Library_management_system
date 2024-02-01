from django.urls import path, include
from rest_framework.routers import DefaultRouter
from book.views import BookView

app_name = "book"

router = DefaultRouter()

router.register("", BookView, basename="books")

urlpatterns = [
    path("", include(router.urls)),
]
