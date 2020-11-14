import pytest
from faker import Factory as FakerFactory
from pytest_factoryboy import register

from cinema.models import Film

from .factories import (
    CinemaFilmPersonProfessionFactory,
    CinemaPersonFactory,
    CinemaPersonWithFilmFactory,
    CinemaProfessionFactory,
    CommentToFilmFactory,
    CommentToNewsFactory,
    CommentToPersonFactory,
    CommentToProductFactory,
    CountryFactory,
    DistributorFactory,
    FilmFactory,
    GenreFactory,
    ImdbRatingFactory,
    LanguageFactory,
    MpaaRatingFactory,
    NewsFactory,
    ProductFactory,
)

faker = FakerFactory.create()

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


@pytest.fixture
def film_fixture(db):
    cinema_persons = []
    for username in (
        "steven.spielberg",
        "jack.nicholson",
        "leonardo.dicaprio",
        "robert.deniro",
        "al.pacino",
        "tom.hanks",
        "quentin.tarantino",
    ):
        first_name, _, last_name = username.partition(".")
        email = f"{username}@hollywood.com"
        cinema_person = CinemaPersonFactory(
            user__first_name=first_name,
            user__last_name=last_name,
            user__username=username,
            user__email=email,
            gender="M",
        )
        cinema_persons.append(cinema_person)

    countries = []
    for country_name in ("USA", "UK", "France", "Italy", "Australia"):
        country = CountryFactory(name=country_name)
        countries.append(country)
    genres = []
    for genre_name in ("Western", "Drama", "Comedy", "Adventure", "Crime"):
        genre = GenreFactory(name=genre_name)
        genres.append(genre)
    languages = []
    for language_name in ("English", "German", "Italian", "French", "Spanish"):
        language = LanguageFactory(name=language_name)
        languages.append(language)
    distributors = []
    for distributor_name in (
        "Columbia Pictures",
        "Paramount Pictures",
        "Universal Pictures",
        "Warner Bros.",
        "Netflix",
    ):
        distributor = DistributorFactory(name=distributor_name)
        distributors.append(distributor)

    film = FilmFactory(
        title="The Greatest Movie",
        country=countries,
        genre=genres,
        distributor=distributors,
    )
    professions = []
    for profession_name in ("Director", "Actor", "Writer"):
        profession = CinemaProfessionFactory(name=profession_name)
        professions.append(profession)

    for i in range(len(cinema_persons)):
        CinemaFilmPersonProfessionFactory(
            cinema_person=cinema_persons[i],
            film=film,
            profession=faker.random_element(professions),
        )
    return Film.objects.get(title="The Greatest Movie")
