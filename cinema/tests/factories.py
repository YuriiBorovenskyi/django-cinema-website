from tempfile import NamedTemporaryFile
import factory
from faker import Factory as FakerFactory

from accounts.tests.factories import UserFactory
from cinema.models import (
    Country,
    Genre,
    ImdbRating,
    MpaaRating,
    Language,
    Distributor,
    CinemaPerson,
    Film,
    CinemaProfession,
    CinemaFilmPersonProfession,
    News,
    Product,
    CommentToPerson,
    CommentToFilm,
    CommentToNews,
    CommentToProduct,
)

faker = FakerFactory.create()


class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country
        django_get_or_create = ('name',)

    name = "USA"


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre

    name = factory.Sequence(lambda n: f"Genre_{n}")


class ImdbRatingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ImdbRating
        django_get_or_create = ('value',)

    value = 8.0


class MpaaRatingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MpaaRating

    value = factory.Sequence(lambda n: f"Rating_{n}")
    description = factory.Faker("text")


class LanguageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Language

    name = factory.Sequence(lambda n: f"Language_{n}")


class DistributorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Distributor

    name = factory.Sequence(lambda n: f"Distributor_{n}")


class CinemaPersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CinemaPerson

    gender = factory.Faker("random_element", elements=('M', 'F'))
    country = factory.SubFactory(CountryFactory)
    birthday = factory.Faker("date_of_birth")
    user = factory.SubFactory(UserFactory)
    bio = factory.Faker("text")
    oscar_awards = factory.Faker("pyint", max_value=12)
    avatar = NamedTemporaryFile(
        suffix=".jpg", dir="/usr/src/app/media/"
    ).name


class CinemaProfessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CinemaProfession
        django_get_or_create = ('name',)

    name = "Actor"


class FilmFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Film

    title = factory.Faker("sentence", nb_words=4)

    @factory.post_generation
    def country(self, create, extracted):
        if not create:
            return
        if extracted:
            for country in extracted:
                self.country.add(country)

    @factory.post_generation
    def genre(self, create, extracted):
        if not create:
            return
        if extracted:
            for genre in extracted:
                self.genre.add(genre)

    budget = factory.Faker("pyint", min_value=10000000, max_value=300000000)
    usa_gross = factory.Faker("pyint", min_value=10000000, max_value=500000000)
    world_gross = factory.Faker(
        "pyint", min_value=10000000, max_value=1000000000
    )
    run_time = factory.Faker("time_delta")
    description = factory.Faker("text")
    release_data = factory.Faker("date_object")

    @factory.post_generation
    def language(self, create, extracted):
        if not create:
            return
        if extracted:
            for language in extracted:
                self.language.add(language)

    @factory.post_generation
    def distributor(self, create, extracted):
        if not create:
            return
        if extracted:
            for distributor in extracted:
                self.distributor.add(distributor)

    imdb_rating = factory.SubFactory(ImdbRatingFactory)
    mpaa_rating = factory.SubFactory(MpaaRatingFactory)
    oscar_awards = factory.Faker("pyint", max_value=12)
    poster = NamedTemporaryFile(
        suffix=".jpg", dir="/usr/src/app/media/"
    ).name


class CinemaFilmPersonProfessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CinemaFilmPersonProfession

    cinema_person = factory.SubFactory(CinemaPersonFactory)
    film = factory.SubFactory(FilmFactory)
    profession = factory.SubFactory(CinemaProfessionFactory)


class CinemaPersonWithFilmFactory(CinemaPersonFactory):
    membership = factory.RelatedFactory(
        CinemaFilmPersonProfessionFactory,
        factory_related_name='cinema_person',
    )


class NewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = News

    title = factory.Faker("sentence")
    description = factory.Faker("text")
    news_source = factory.Faker("word")
    news_author = factory.Faker("name")

    @factory.post_generation
    def film(self, create, extracted):
        if not create:
            return
        if extracted:
            for film in extracted:
                self.film.add(film)

    @factory.post_generation
    def cinema_person(self, create, extracted):
        if not create:
            return
        if extracted:
            for person in extracted:
                self.cinema_person.add(person)

    news_feed_photo = NamedTemporaryFile(
        suffix=".jpg", dir="/usr/src/app/media/"
    ).name
    news_detail_photo = NamedTemporaryFile(
        suffix=".jpg", dir="/usr/src/app/media/"
    ).name
    created_at = factory.Faker("date_time")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    price = factory.Faker(
        "pyfloat", right_digits=2, max_value=200, positive=True
    )
    in_stock = factory.Faker("pyint", max_value=100)
    film = factory.SubFactory(FilmFactory)
    created_at = factory.Faker("date_time")


class CommentToPersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CommentToPerson

    author = factory.Faker("name")
    content = factory.Faker("text")
    is_active = factory.Faker("pybool")
    cinema_person = factory.SubFactory(CinemaPersonFactory)
    created_at = factory.Faker("date_time")


class CommentToFilmFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CommentToFilm

    author = factory.Faker("name")
    content = factory.Faker("text")
    is_active = factory.Faker("pybool")
    film = factory.SubFactory(FilmFactory)
    created_at = factory.Faker("date_time")


class CommentToNewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CommentToNews

    author = factory.Faker("name")
    content = factory.Faker("text")
    is_active = factory.Faker("pybool")
    news = factory.SubFactory(NewsFactory)
    created_at = factory.Faker("date_time")


class CommentToProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CommentToProduct

    author = factory.Faker("name")
    content = factory.Faker("text")
    is_active = factory.Faker("pybool")
    product = factory.SubFactory(ProductFactory)
    created_at = factory.Faker("date_time")
