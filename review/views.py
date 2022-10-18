from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from rest_framework.authentication import TokenAuthentication

from users.models import User
from .serializers import ReviewSerializer
from .permissions import ReviewDetailPermissions, ReviewPermissions
from .models import Review
from movie.models import Movie


class ReviewView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ReviewPermissions]

    def get(self, request: Request, movie_id: int):
        reviews = Review.objects.filter(movie_id=movie_id)

        result_page = self.paginate_queryset(reviews, request, view=self)
        serializer = ReviewSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request, movie_id: int):
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = ReviewSerializer(data=request.data)
        self.check_object_permissions(request, serializer)
        serializer.is_valid(raise_exception=True)

        if len(movie.reviews.filter(critic_id=request.user.id)) > 0:
            return Response(
                {"detail": "Review already registred"}, status.HTTP_403_FORBIDDEN
            )

        serializer.save(movie_id=movie_id, critic=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)


class ReviewDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ReviewDetailPermissions]

    def get(self, request: Request, movie_id: int, review_id: int):
        movie = get_object_or_404(Movie, id=movie_id)
        try:
            review = movie.reviews.get(id=review_id)
        except Http404:
            return Response({"detail": "Review not found"}, status.HTTP_404_NOT_FOUND)

        serializer = ReviewSerializer(review)

        return Response(serializer.data)

    def delete(self, request: Request, movie_id: int, review_id: int):
        movie = get_object_or_404(Movie, id=movie_id)

        try:
            review = movie.reviews.get(id=review_id)
            self.check_object_permissions(request, review)
        except review.DoesNotExist:
            return Response({"detail": "Review not found"}, status.HTTP_404_NOT_FOUND)

        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
