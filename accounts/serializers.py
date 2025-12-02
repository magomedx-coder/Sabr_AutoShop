from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

from .models import RoleChoices, UserProfile

User = get_user_model()


class UserSerializer(BaseUserSerializer):
    role = serializers.CharField(source="profile.role", read_only=True)

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = (*BaseUserSerializer.Meta.fields, "role")


class UserCreateSerializer(BaseUserCreateSerializer):
    role = serializers.ChoiceField(choices=RoleChoices.choices, source="profile.role", default=RoleChoices.BUYER)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = (*BaseUserCreateSerializer.Meta.fields, "role")

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", {})
        user = super().create(validated_data)
        role = profile_data.get("role", RoleChoices.BUYER)
        UserProfile.objects.update_or_create(user=user, defaults={"role": role})
        return user