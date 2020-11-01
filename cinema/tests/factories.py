import factory
from faker import Factory as FakerFactory

from django.utils.timezone import now

from cinema.models import (
    Country,
    Genre,
    ImdbRating,
    MpaaRating,
    Language,
    Distributor,
)

faker = FakerFactory.create()


class CountryFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("country")
    
    class Meta:
        model = Country


class GenreFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("word")
    
    class Meta:
        model = Genre


class ImdbRatingFactory(factory.django.DjangoModelFactory):
    value = factory.Faker(
        "pyfloat", left_digits=1, right_digits=1, positive=True
    )

    class Meta:
        model = ImdbRating


class MpaaRatingFactory(factory.django.DjangoModelFactory):
    value = factory.Faker("word")
    description = factory.Faker("text", max_nb_chars=64)

    class Meta:
        model = MpaaRating


class LanguageFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("language_name")

    class Meta:
        model = Language


class DistributorFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("company")

    class Meta:
        model = Distributor


# random_choices(['M', 'F'], 1)
