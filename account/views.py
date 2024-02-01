from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import AllowAny
from account.models import User
from account.serializers import UserListSerializer, UserDetailSerializer


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
