from rest_framework import serializers
from users.models import User


class Validators:
    def username(username: str) -> str:
        username_already_exists = User.objects.filter(username=username).exists()

        if username_already_exists:
            raise serializers.ValidationError("Username already exists")

        return username

    def email(email: str) -> str:
        email_already_exists = User.objects.filter(email=email).exists()

        if email_already_exists:
            raise serializers.ValidationError("Email already exists")

        return email

    def stars(stars: str) -> str:
        if stars > 10:
            raise serializers.ValidationError(
                "Ensure this value is less than or equal to 10."
            )
        elif stars <= 0:
            raise serializers.ValidationError(
                "Ensure this value is greater than or equal to 1"
            )

        return stars
