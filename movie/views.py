from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from rest_framework.authentication import TokenAuthentication
from .serializers import MovieSerializer
from .permissions import MoviePermissions
from .models import Movie


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [MoviePermissions]

    def get(self, request: Request):
        movie = Movie.objects.all()

        result_page = self.paginate_queryset(movie, request, view=self)
        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request):
        serializer = MovieSerializer(data=request.data)

        self.check_object_permissions(request, serializer)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class MovieDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [MoviePermissions]

    def get(self, request: Request, movie_id: int):
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieSerializer(movie)
        self.check_object_permissions(request, serializer)

        return Response(serializer.data)

    def patch(self, request: Request, movie_id: int):
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieSerializer(movie, request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request: Request, movie_id: int):
        movie = get_object_or_404(Movie, id=movie_id)

        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
