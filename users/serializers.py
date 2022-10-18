from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        max_length=20,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="username already exists",
            )
        ],
    )
    email = serializers.EmailField(
        max_length=20,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="email already exists",
            )
        ],
    )
    birthdate = serializers.DateField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    bio = serializers.CharField(allow_null=True, default="")
    is_critic = serializers.BooleanField(allow_null=True, default=False)
    updated_at = serializers.DateTimeField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True, default=False)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CriticSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)
