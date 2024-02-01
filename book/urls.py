from django.urls import path, include
from rest_framework.routers import DefaultRouter
from book.views import BookView, BorrowedBooksView, BorrowedBooksListView

app_name = "book"

router = DefaultRouter()
router.register("book", BookView, basename="books")
router.register("borrowed", BorrowedBooksView, basename="borrowed_books")

urlpatterns = [
    path("", include(router.urls)),
]
