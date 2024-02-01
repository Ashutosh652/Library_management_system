from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny
from book.models import Book
from book.serializers import BookListSerializer, BookDetailSerializer


class BookView(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
):
    """View to list/retrieve/create/update books."""

    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"

    def get_serializer_class(self):
        """Return the appropriate serializer class based on the action."""
        serializer_action_classes = {
            "list": BookListSerializer,
            "retrieve": BookDetailSerializer,
            "create": BookDetailSerializer,
            "update": BookDetailSerializer,
            "partial_update": BookDetailSerializer,
        }
        return (
            serializer_action_classes[self.action]
            if self.action in serializer_action_classes
            else self.serializer_class
        )
