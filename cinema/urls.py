from django.urls import path

from .apps import CinemaConfig
from .views import (ProductListView, product_detail, NewsListView,
                    news_detail, film_detail, cinema_person_detail,
                    FilmListView, TopRatedProductListView,
                    NewReleasesProductListView, CelebrityNewsListView,
                    TopRatedFilmListView, BudgetFilmListView,
                    UsaGrossFilmListView, WorldGrossFilmListView,
                    SearchResultsView, YearFilmListView, GenreFilmListView,
                    CountryFilmListView, LanguageFilmListView, MpaaFilmListView,
                    DistributorFilmListView, IndexView)


app_name = CinemaConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('blu-ray/', ProductListView.as_view(), name='product-list'),
    path('film/', FilmListView.as_view(), name='film-list'),
    path('news/', NewsListView.as_view(), name='news-list'),
    path('search/', SearchResultsView.as_view(), name='search-results'),
    path('blu-ray/top-rated/', TopRatedProductListView.as_view(),
         name='top-rated-product-list'),
    path('blu-ray/new-releases/', NewReleasesProductListView.as_view(),
         name='new-releases-product-list'),
    path('film/top-rated/', TopRatedFilmListView.as_view(),
         name='top-rated-film-list'),
    path('film/budget/', BudgetFilmListView.as_view(),
         name='budget-film-list'),
    path('film/usa-gross/', UsaGrossFilmListView.as_view(),
         name='usa-gross-film-list'),
    path('film/world-gross/', WorldGrossFilmListView.as_view(),
         name='world-gross-film-list'),
    path('news/celebrity/', CelebrityNewsListView.as_view(),
         name='celebrity-news-list'),
    path('blu-ray/<int:pk>/', product_detail, name='product-detail'),
    path('film/<int:pk>/', film_detail, name='film-detail'),
    path('movie-person/<int:pk>/', cinema_person_detail,
         name='movie-person-detail'),
    path('news/<int:pk>/', news_detail, name='news-detail'),
    path('film/year/<int:year>/', YearFilmListView.as_view(),
         name='year-film-list'),
    path('film/genre/<str:genre>/', GenreFilmListView.as_view(),
         name='genre-film-list'),
    path('film/country/<str:country>/', CountryFilmListView.as_view(),
         name='country-film-list'),
    path('film/language/<str:language>/', LanguageFilmListView.as_view(),
         name='language-film-list'),
    path('film/mpaa/<int:pk>/', MpaaFilmListView.as_view(),
         name='mpaa-film-list'),
    path('film/distributor/<str:distributor>/',
         DistributorFilmListView.as_view(), name='distributor-film-list'),
]
