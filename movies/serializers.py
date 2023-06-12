from rest_framework import serializers
from genres.serializers import GenreSerializer
from .models import Movie
from genres.models import Genre


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10)
    premiere = serializers.DateField()
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()

    genres = GenreSerializer(many=True)

    def create(self, validated_data: dict) -> Movie:
        genres = validated_data.pop("genres")

        movie = Movie.objects.create(**validated_data)
        for genre in genres:
            new_genre = Genre.objects.get_or_create(**genre)
            movie.genres.add(new_genre[0])

        return movie

    def update(self, instance: Movie, validated_data: dict) -> Movie:
        genres = validated_data.pop("genres")
        movie = Movie.objects.filter(id=validated_data["id"]).first()
        movie.genres.clear()

        for genre in genres:
            new_genre = Genre.objects.get_or_create(**genre)
            movie.genres.add(new_genre[0])

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
