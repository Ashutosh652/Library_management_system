from rest_framework import serializers
from account.models import User


class UserListSerializer(serializers.ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(
        view_name="account:users-detail", lookup_field="id"
    )

    class Meta:
        model = User
        fields = ("id", "detail", "email", "first_name", "last_name")


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "membership_date",
            "is_staff",
            "is_active",
            "is_superuser",
        )
