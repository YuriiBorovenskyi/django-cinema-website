from django.urls import path

from .views import (
    FilmListView, FilmDetailView, comments_to_film,
    NewsListView, NewsDetailView, comments_to_news,
    CinemaPersonDetailView, comments_to_person,
)

urlpatterns = [
    path('films/', FilmListView.as_view()),
    path('news/', NewsListView.as_view()),
    path('films/<int:pk>/', FilmDetailView.as_view()),
    path('news/<int:pk>/', NewsDetailView.as_view()),
    path('movie-persons/<int:pk>/', CinemaPersonDetailView.as_view()),
    path('films/<int:pk>/comments/', comments_to_film),
    path('news/<int:pk>/comments/', comments_to_news),
    path('movie-persons/<int:pk>/comments/', comments_to_person),
]
