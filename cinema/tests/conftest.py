import pytest
from pytest_factoryboy import register

from .factories import (
    CountryFactory,
    GenreFactory,
    ImdbRatingFactory,
    MpaaRatingFactory,
    LanguageFactory,
    DistributorFactory,
)

register(CountryFactory)
register(GenreFactory)
register(ImdbRatingFactory)
register(MpaaRatingFactory)
register(LanguageFactory)
register(DistributorFactory)

