from rest_framework import serializers
from utils import DuplicateValueError, Validators

from users.models import User
from .models import Review


class CriticSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")


class ReviewSerializer(serializers.ModelSerializer):
    critic = CriticSerializer(source="user", read_only=True)

    class Meta:
        model = Review

        fields = (
            "id",
            "stars",
            "review",
            "spoilers",
            "recomendation",
            "movie_id",
            "critic",
        )

        read_only_fields = ["movie_id"]

    def validate_stars(self, value):
        return Validators.stars(value)

    def create(self, validated_data: dict) -> Review:
        errors = {}

        movie = validated_data.pop("movie")
        critic = validated_data.pop("user")
        reviews = Review.objects.filter(movie=movie)

        for review in reviews:
            if review.user == critic:
                errors.update({"detail": "Review already exists."})

        if bool(errors):
            raise DuplicateValueError(errors)

        review = Review.objects.create(
            **{**validated_data, "movie": movie, "user": critic}
        )

        return review
