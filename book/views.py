from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from book.models import Book, BorrowedBooks
from account.models import User
from book.serializers import (
    BookListSerializer,
    BookDetailSerializer,
    BorrowedBooksListSerializer,
    BorrowBookSerializer,
    ReturnBookSerializer,
)
from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


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
    authentication_classes = [CsrfExemptSessionAuthentication]
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


class BorrowedBooksView(GenericViewSet, ListModelMixin):
    """View to create/retrieve/list borrowed books."""

    queryset = BorrowedBooks.objects.all()
    serializer_class = BorrowedBooksListSerializer
    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]

    @extend_schema(request=BorrowBookSerializer, responses=BorrowedBooksListSerializer)
    @action(detail=False, methods=["post"], serializer_class=BorrowBookSerializer)
    def borrow_book(self, request, pk=None):
        """Endpoint to record the borrowing of a book by linking a user with a book."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data["user_id"]
        book_id = serializer.validated_data["book_id"]
        borrow_date = serializer.validated_data["borrow_date"]
        try:
            user = User.objects.get(pk=user_id)
            book = Book.objects.get(pk=book_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Book.DoesNotExist:
            return Response(
                {"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if BorrowedBooks.objects.filter(user=user, book=book).exists():
            return Response(
                {"detail": "This user has already borrowed the same book."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        borrowed_book = BorrowedBooks.objects.create(
            user=user, book=book, borrow_date=borrow_date
        )
        response_serializer = BorrowedBooksListSerializer(borrowed_book)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=ReturnBookSerializer, responses=BorrowedBooksListSerializer)
    @action(detail=False, methods=["post"], serializer_class=ReturnBookSerializer)
    def return_book(self, request, pk=None):
        """Endpoint to record the borrowing of a book by linking a user with a book."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data["user_id"]
        book_id = serializer.validated_data["book_id"]
        return_date = serializer.validated_data["return_date"]
        try:
            user = User.objects.get(pk=user_id)
            book = Book.objects.get(pk=book_id)
            borrowed_book = BorrowedBooks.objects.get(user=user, book=book)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Book.DoesNotExist:
            return Response(
                {"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except BorrowedBooks.DoesNotExist:
            return Response(
                {"detail": "The book has not been borrowed by the user."},
                status=status.HTTP_404_NOT_FOUND,
            )
        borrowed_book.return_date = return_date
        borrowed_book.save()
        response_serializer = BorrowedBooksListSerializer(borrowed_book)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
