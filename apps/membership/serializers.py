from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from apps.membership.models import User


class CustomUserSerializer(ModelSerializer):
    """
    Serializer for the custom User model.
    """

    class Meta:
        model = User
        fields = (
            'id',
            'email',
        )


class LoginUserSerializer(Serializer):
    """
    Serializer for user authentication during login.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validates user credentials.
        """
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError(_('Incorrect credentials!'))


class RegisterUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data['email'], password=validated_data['password'])
        return user
