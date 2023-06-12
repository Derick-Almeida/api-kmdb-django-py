from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination

from .serializers import ReviewSerializer
from .models import Review
from movies.models import Movie

from utils import IsAdminOrReadyOnly, IsCriticAndReviewOwner, IsAdminOrCritic


class ReviewView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrCritic]

    def get(self, req: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        reviews = Review.objects.filter(movie=movie)
        result_page = self.paginate_queryset(reviews, req, view=self)
        serializer = ReviewSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, req: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = ReviewSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=req.user, movie=movie)

        return Response(serializer.data, status.HTTP_201_CREATED)


class ReviewDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadyOnly | IsCriticAndReviewOwner]

    def get(self, req: Request, movie_id: int, review_id: int) -> Response:
        get_object_or_404(Movie, id=movie_id)
        review = get_object_or_404(Review, id=review_id)

        serializer = ReviewSerializer(review)

        return Response(serializer.data)

    def delete(self, req: Request, movie_id: int, review_id: int) -> Response:
        get_object_or_404(Movie, id=movie_id)
        review = get_object_or_404(Review, id=review_id)

        self.check_object_permissions(req, review)

        review.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
