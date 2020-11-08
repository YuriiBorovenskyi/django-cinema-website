from os.path import isdir
from shutil import rmtree
from uuid import uuid4

import pytest
from pytest_factoryboy import register
from faker import Factory as FakerFactory

from .factories import (
    CountryFactory,
    GenreFactory,
    ImdbRatingFactory,
    MpaaRatingFactory,
    LanguageFactory,
    DistributorFactory,
    CinemaPersonFactory,
    CinemaProfessionFactory,
    FilmFactory,
    CinemaFilmPersonProfessionFactory,
    CinemaPersonWithFilmFactory,
    NewsFactory,
    ProductFactory,
    CommentToPersonFactory,
    CommentToFilmFactory,
    CommentToNewsFactory,
    CommentToProductFactory,
)
from cinema.models import Film

faker = FakerFactory.create()

country_names = ["USA", "UK", "France", "Italy", "Australia"]
genre_names = ["Western", "Drama", "Comedy", "Adventure", "Crime"]
imdb_ratings = [8.0, 8.5, 9.0]
mpaa_ratings = ["PG-13", "R", "Not Rated"]
mpaa_descriptions = [
    "Children under 13", "Children under 17", "The upcoming movie"
]
language_names = ["English", "German", "Italian", "French", "Spanish"]
distributor_names = [
    "Columbia Pictures", "Paramount Pictures",
    "Universal Pictures", "Warner Bros.", "Netflix"
]
usernames = [
    "steven.spielberg", "jack.nicholson", "leonardo.dicaprio",
    "robert.deniro", "al.pacino", "tom.hanks", "quentin.tarantino"
]
profession_names = ["Director", "Actor", "Writer"]

register(CountryFactory)
register(GenreFactory)
register(ImdbRatingFactory)
register(MpaaRatingFactory)
register(LanguageFactory)
register(DistributorFactory)
register(CinemaPersonFactory)
register(CinemaProfessionFactory)
register(FilmFactory)
register(CinemaFilmPersonProfessionFactory)
register(CinemaPersonWithFilmFactory)
register(NewsFactory)
register(ProductFactory)
register(CommentToPersonFactory)
register(CommentToFilmFactory)
register(CommentToNewsFactory)
register(CommentToProductFactory)


@pytest.fixture()
def film_fixture(db):
    cinema_persons = []
    for username in usernames:
        first_name, _, last_name = username.partition('.')
        email = f"{username}@hollywood.com"
        cinema_person = CinemaPersonFactory(
            user__first_name=first_name, user__last_name=last_name,
            user__username=username,
            user__email=email,
            gender='M',
        )
        cinema_persons.append(cinema_person)

    countries = []
    for country_name in country_names:
        country = CountryFactory(name=country_name)
        countries.append(country)
    genres = []
    for genre_name in genre_names:
        genre = GenreFactory(name=genre_name)
        genres.append(genre)
    languages = []
    for language_name in language_names:
        language = LanguageFactory(name=language_name)
        languages.append(language)
    distributors = []
    for distributor_name in distributor_names:
        distributor = DistributorFactory(name=distributor_name)
        distributors.append(distributor)

    film = FilmFactory(
        title="The Greatest Movie", country=countries,
        genre=genres, distributor=distributors,
    )
    professions = []
    for profession_name in profession_names:
        profession = CinemaProfessionFactory(name=profession_name)
        professions.append(profession)

    for i in range(len(cinema_persons)):
        CinemaFilmPersonProfessionFactory(
            cinema_person=cinema_persons[i],
            film=film,
            profession=faker.random_element(professions)
        )
    return Film.objects.get(title="The Greatest Movie")


# def get_path_to_keep_test_image():
#     return f"tests/{uuid4().hex}.jpg"


# @pytest.fixture()
# def cinema_person_factory(mocker):
#     mocker.patch(
#         "cinema.models.upload_to_cinema_person",
#         get_path_to_keep_test_image
#     )
#     return CinemaPersonFactory


# @pytest.fixture(scope="class")
# def clean_test_media():
#     yield
#
#     test_media_path = "/usr/src/app/media/tests"
#     if isdir(test_media_path):
#         rmtree(test_media_path)
