from rest_framework import serializers
from .models import User
from utils import Validators


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


class RegisterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=20)
    email = serializers.EmailField(max_length=127)
    password = serializers.CharField(max_length=100, write_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField()
    bio = serializers.CharField(allow_null=True, default=None)
    is_critic = serializers.BooleanField(allow_null=True, default=False)
    updated_at = serializers.DateTimeField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    def validate_username(self, value):
        return Validators.username(value)

    def validate_email(self, value):
        return Validators.email(value)

    def create(self, validated_data: User) -> User:
        user = User.objects.create_user(**validated_data)

        return user
