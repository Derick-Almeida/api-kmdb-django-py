from django.urls import path
from . import views as movie_views
from reviews import views as review_views

urlpatterns = [
    path("movies/", movie_views.MovieView.as_view()),
    path("movies/<int:movie_id>/", movie_views.MovieDetailView.as_view()),
    path("movies/<int:movie_id>/reviews/", review_views.ReviewView.as_view()),
    path(
        "movies/<int:movie_id>/reviews/<int:review_id>/",
        review_views.ReviewDetailView.as_view(),
    ),
]
