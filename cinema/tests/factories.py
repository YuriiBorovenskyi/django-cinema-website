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

    title = factory.Faker("sentence", nb_words=3)

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


# class FooFactory(factory.Factory):
#     class Meta:
#         model = Foo
#     # Generate a list of `factory` objects of random size, ranging from 1 -> 5
#     bar = factory.RelatedFactoryList(BarFactory, size=lambda: random.randint(1, 5))
#     # Each Foo object will have exactly 3 Bar objects generated for its foobar attribute.
#     foobar = factory.RelatedFactoryList(BarFactory, size=3)
