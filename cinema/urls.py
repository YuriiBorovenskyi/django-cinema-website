from django.urls import path

from .apps import CinemaConfig
from .views import (
    ProductListView, product_detail, NewsListView, news_detail, film_detail,
    cinema_person_detail, FilmListView, TopRatedProductListView,
    NewReleasesProductListView, CelebrityNewsListView, TopRatedFilmListView,
    BudgetFilmListView, UsaGrossFilmListView, WorldGrossFilmListView,
    SearchResultsView, YearFilmListView, GenreFilmListView,
    CountryFilmListView, LanguageFilmListView, MpaaFilmListView,
    DistributorFilmListView, IndexView
)

app_name = CinemaConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('blu-ray-films/', ProductListView.as_view(), name='product-list'),
    path('films/', FilmListView.as_view(), name='film-list'),
    path('news/', NewsListView.as_view(), name='news-list'),
    path('search/', SearchResultsView.as_view(), name='search-results'),
    path('blu-ray-films/by-top-rated/', TopRatedProductListView.as_view(),
         name='top-rated-product-list'),
    path('blu-ray-films/new-releases/', NewReleasesProductListView.as_view(),
         name='new-releases-product-list'),
    path('films/by-top-rated/', TopRatedFilmListView.as_view(),
         name='top-rated-film-list'),
    path('films/by-budget/', BudgetFilmListView.as_view(),
         name='budget-film-list'),
    path('films/by-usa-gross/', UsaGrossFilmListView.as_view(),
         name='usa-gross-film-list'),
    path('films/by-world-gross/', WorldGrossFilmListView.as_view(),
         name='world-gross-film-list'),
    path('news/celebrities/', CelebrityNewsListView.as_view(),
         name='celebrity-news-list'),
    path('blu-ray-films/<int:pk>/', product_detail, name='product-detail'),
    path('films/<int:pk>/', film_detail, name='film-detail'),
    path('movie-persons/<int:pk>/', cinema_person_detail,
         name='movie-person-detail'),
    path('news/<int:pk>/', news_detail, name='news-detail'),
    path('films/by-year/<int:year>/', YearFilmListView.as_view(),
         name='year-film-list'),
    path('films/by-genre/<str:genre>/', GenreFilmListView.as_view(),
         name='genre-film-list'),
    path('films/by-country/<str:country>/', CountryFilmListView.as_view(),
         name='country-film-list'),
    path('films/by-language/<str:language>/', LanguageFilmListView.as_view(),
         name='language-film-list'),
    path('films/by-mpaa/<int:pk>/', MpaaFilmListView.as_view(),
         name='mpaa-film-list'),
    path('films/by-distributor/<str:distributor>/',
         DistributorFilmListView.as_view(), name='distributor-film-list'),
]
