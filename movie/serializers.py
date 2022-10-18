import ipdb

from rest_framework import serializers

from genre.models import Genre

from .models import Movie

from genre.serializers import GenreSerializer


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    duration = serializers.CharField()
    classification = serializers.IntegerField()
    premiere = serializers.DateField()
    synopsis = serializers.CharField()

    genres = GenreSerializer(many=True)

    def create(self, validated_data: dict):
        genres = validated_data.pop("genres")

        movie = Movie.objects.create(**validated_data)

        for genre in genres:
            actual_genre, _ = Genre.objects.get_or_create(**genre)
            movie.genres.add(actual_genre)

        return movie

    def update(self, instance, validated_data: dict):
        genre_data = validated_data.pop("genres")

        genre_list: list = []

        for key, value in validated_data.items():
            setattr(instance, key, value)

        for genre in genre_data:
            new_genre = Genre.objects.create(**genre)
            genre_list.append(new_genre)

        instance.genres.set(genre_list)
        instance.save()
        return instance
