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
def test_film(db):
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
        first_name, _, last_name = username.title().partition(".")
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
        title="The Greatest Show On The World",
        country=countries,
        genre=genres,
        language=languages,
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
    return Film.objects.first()


@pytest.fixture
def test_product(db, test_film):
    return ProductFactory(film=test_film)


@pytest.fixture
def test_person(db, test_film):
    return test_film.staff.first()


@pytest.fixture
def test_news(db, test_film):
    return NewsFactory(film=(test_film,))


@pytest.fixture
def create_12_films(db):
    country_1 = CountryFactory(name="USA")
    country_2 = CountryFactory(name="France")
    genre_1 = GenreFactory(name="Drama")
    genre_2 = GenreFactory(name="Comedian")
    language_1 = LanguageFactory(name="English")
    language_2 = LanguageFactory(name="German")
    distributor_1 = DistributorFactory(name="Columbia Pictures")
    distributor_2 = DistributorFactory(name="Paramount Pictures")

    for _ in range(6):
        CinemaFilmPersonProfessionFactory.create(
            film=FilmFactory(
                country=(country_1,),
                genre=(genre_1,),
                language=(language_1,),
                distributor=(distributor_1,),
            ),
        )
    for _ in range(6):
        CinemaFilmPersonProfessionFactory.create(
            film=FilmFactory(
                country=(country_2,),
                genre=(genre_2,),
                language=(language_2,),
                distributor=(distributor_2,),
            ),
        )


@pytest.fixture
def create_12_products(db, create_12_films):
    for film in Film.objects.all():
        ProductFactory.create(film=film)


@pytest.fixture
def create_12_news(db, create_12_films):
    for film in Film.objects.all():
        NewsFactory.create(film=(film,))


@pytest.fixture
def create_12_films_products_news(db, create_12_films):
    for film in Film.objects.all():
        ProductFactory.create(film=film)
        NewsFactory.create(film=(film,))
