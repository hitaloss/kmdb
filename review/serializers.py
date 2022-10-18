from rest_framework import serializers
from .models import Review
from users.serializers import CriticSerializer


class ReviewSerializer(serializers.ModelSerializer):
    critic = CriticSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "stars",
            "review",
            "spoilers",
            "recomendation",
            "movie_id",
            "critic",
        ]
        depth = 1
        read_only_fields = ["movie_id"]
