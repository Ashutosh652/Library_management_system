from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from account.models import User
from account.serializers import UserListSerializer, UserDetailSerializer
from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class UserView(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """View to list/retrieve/create the users."""

    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"

    def get_serializer_class(self):
        """Return the appropriate serializer class based on the action."""
        serializer_action_classes = {
            "list": UserListSerializer,
            "retrieve": UserDetailSerializer,
        }
        return (
            serializer_action_classes[self.action]
            if self.action in serializer_action_classes
            else self.serializer_class
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return Response(
                {"detail": "Logged in successfully."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "Email or Password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogoutView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        logout(request)
        return Response(
            {"detail": "Logged out successfully."}, status=status.HTTP_200_OK
        )
