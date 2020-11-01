import pytest

from cinema.models import (
    Country,
    Genre,
    ImdbRating,
    MpaaRating,
    Language,
    Distributor,
)

country_names = ["USA", "UK", "France", "Italy", "Australia"]
genre_names = ["Crime", "Drama", "Comedy", "Adventure", "Western"]
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


@pytest.mark.django_db
class TestCountryModel:
    label_argvalues = [("name", "name"), ]
    label_ids = [
        f"'{arg[0]}' field: is label '{arg[1]}'?"
        for arg in label_argvalues
    ]
    field_argvalues = [
        ("name", "max_length", 64),
        ("name", "unique", True),
    ]
    field_ids = [
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?"
        for arg in field_argvalues
    ]

    def test_record_is_instance_of_model(self, country):
        assert isinstance(country, Country)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_argvalues,
        ids=label_ids
    )
    def test_label_of_model_field(
            self, country, field_name, expected_label
    ):
        actual_label = country._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_argvalues,
        ids=field_ids
    )
    def test_options_of_model_fields(
            self, country, field_name, option_name, expected_option_value
    ):
        if option_name == "max_length":
            actual_option_value = country._meta.get_field(field_name).max_length
        elif option_name == "unique":
            actual_option_value = country._meta.get_field(field_name).unique
        else:
            raise AttributeError(
                f"String '{option_name}' cannot be an attribute."
            )
        assert actual_option_value == expected_option_value

    def test_record_string_representation_is_country_name(self, country):
        expected_result_of_method_str = country.name
        assert str(country) == expected_result_of_method_str

    def test_values_of_record_fields(self, country_factory):
        country = country_factory(name=country_names[0])
        actual_name = country.name
        expected_name = country_names[0]
        assert actual_name, expected_name
        assert Country.objects.count() == 1


@pytest.mark.django_db
class TestGenreModel:
    label_argvalues = [("name", "name"), ]
    label_ids = [
        f"'{arg[0]}' field: is label '{arg[1]}'?"
        for arg in label_argvalues
    ]
    field_argvalues = [
        ("name", "max_length", 16),
        ("name", "unique", True),
    ]
    field_ids = [
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?"
        for arg in field_argvalues
    ]

    def test_record_is_instance_of_model(self, genre):
        assert isinstance(genre, Genre)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_argvalues,
        ids=label_ids
    )
    def test_label_of_model_field(
            self, genre, field_name, expected_label
    ):
        actual_label = genre._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_argvalues,
        ids=field_ids
    )
    def test_options_of_model_fields(
            self, genre, field_name, option_name, expected_option_value
    ):
        if option_name == "max_length":
            actual_option_value = genre._meta.get_field(field_name).max_length
        elif option_name == "unique":
            actual_option_value = genre._meta.get_field(field_name).unique
        else:
            raise AttributeError(
                f"String '{option_name}' cannot be an attribute."
            )
        assert actual_option_value == expected_option_value

    def test_record_string_representation_is_genre_name(self, genre):
        expected_result_of_method_str = genre.name
        assert str(genre) == expected_result_of_method_str

    def test_values_of_record_fields(self, genre_factory):
        genre = genre_factory(name=genre_names[0])
        actual_name = genre.name
        expected_name = genre_names[0]
        assert actual_name, expected_name
        assert Genre.objects.count() == 1


@pytest.mark.django_db
class TestImdbRatingModel:
    label_argvalues = [("value", "value"), ]
    label_ids = [
        f"'{arg[0]}' field: is label '{arg[1]}'?"
        for arg in label_argvalues
    ]
    field_argvalues = [
        ("value", "max_digits", 2),
        ("value", "decimal_places", 1),
        ("value", "unique", True),
    ]
    field_ids = [
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?"
        for arg in field_argvalues
    ]

    def test_record_is_instance_of_model(self, imdb_rating):
        assert isinstance(imdb_rating, ImdbRating)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_argvalues,
        ids=label_ids
    )
    def test_label_of_model_field(
            self, imdb_rating, field_name, expected_label
    ):
        actual_label = imdb_rating._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_argvalues,
        ids=field_ids
    )
    def test_options_of_model_fields(
            self, imdb_rating, field_name, option_name, expected_option_value
    ):
        if option_name == "max_digits":
            actual_option_value = imdb_rating._meta.get_field(
                field_name
            ).max_digits
        elif option_name == "decimal_places":
            actual_option_value = imdb_rating._meta.get_field(
                field_name
            ).decimal_places
        elif option_name == "unique":
            actual_option_value = imdb_rating._meta.get_field(field_name).unique
        else:
            raise AttributeError(
                f"String '{option_name}' cannot be an attribute."
            )
        assert actual_option_value == expected_option_value

    def test_record_string_representation_is_imdb_rating_value(
            self, imdb_rating
    ):
        expected_result_of_method_str = str(imdb_rating.value)
        assert str(imdb_rating) == expected_result_of_method_str

    def test_values_of_record_fields(self, imdb_rating_factory):
        imdb_rating = imdb_rating_factory(value=imdb_ratings[0])
        actual_value = imdb_rating.value
        expected_value = imdb_ratings[0]
        assert actual_value, expected_value
        assert ImdbRating.objects.count() == 1


@pytest.mark.django_db
class TestMpaaRatingModel:
    label_argvalues = [
        ("value", "value"),
        ("description", "description"),
    ]
    label_ids = [
        f"'{arg[0]}' field: is label '{arg[1]}'?"
        for arg in label_argvalues
    ]
    field_argvalues = [
        ("value", "max_length", 10),
        ("value", "unique", True),
        ("description", "max_length", 512),
        ("description", "unique", True),
    ]
    field_ids = [
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?"
        for arg in field_argvalues
    ]

    def test_record_is_instance_of_model(self, mpaa_rating):
        assert isinstance(mpaa_rating, MpaaRating)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_argvalues,
        ids=label_ids
    )
    def test_label_of_model_field(
            self, mpaa_rating, field_name, expected_label
    ):
        actual_label = mpaa_rating._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_argvalues,
        ids=field_ids
    )
    def test_options_of_model_fields(
            self, mpaa_rating, field_name, option_name, expected_option_value
    ):
        if option_name == "max_length":
            actual_option_value = mpaa_rating._meta.get_field(
                field_name
            ).max_length
        elif option_name == "unique":
            actual_option_value = mpaa_rating._meta.get_field(field_name).unique
        else:
            raise AttributeError(
                f"String '{option_name}' cannot be an attribute."
            )
        assert actual_option_value == expected_option_value

    def test_record_string_representation_is_mpaa_rating_value(
            self, mpaa_rating
    ):
        expected_result_of_method_str = str(mpaa_rating.value)
        assert str(mpaa_rating) == expected_result_of_method_str

    def test_values_of_record_fields(self, mpaa_rating_factory):
        mpaa_rating = mpaa_rating_factory(
            value=mpaa_ratings[0], description=mpaa_descriptions[0]
        )
        actual_value = mpaa_rating.value
        actual_description = mpaa_rating.description
        expected_value = mpaa_ratings[0]
        expected_description = mpaa_descriptions[0]
        assert actual_value, expected_value
        assert actual_description, expected_description
        assert MpaaRating.objects.count() == 1


@pytest.mark.django_db
class TestLanguageModel:
    label_argvalues = [("name", "name"), ]
    label_ids = [
        f"'{arg[0]}' field: is label '{arg[1]}'?"
        for arg in label_argvalues
    ]
    field_argvalues = [
        ("name", "max_length", 16),
        ("name", "unique", True),
    ]
    field_ids = [
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?"
        for arg in field_argvalues
    ]

    def test_record_is_instance_of_model(self, language):
        assert isinstance(language, Language)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_argvalues,
        ids=label_ids
    )
    def test_label_of_model_field(
            self, language, field_name, expected_label
    ):
        actual_label = language._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_argvalues,
        ids=field_ids
    )
    def test_options_of_model_fields(
            self, language, field_name, option_name, expected_option_value
    ):
        if option_name == "max_length":
            actual_option_value = language._meta.get_field(
                field_name
            ).max_length
        elif option_name == "unique":
            actual_option_value = language._meta.get_field(field_name).unique
        else:
            raise AttributeError(
                f"String '{option_name}' cannot be an attribute."
            )
        assert actual_option_value == expected_option_value

    def test_record_string_representation_is_language_name(self, language):
        expected_result_of_method_str = language.name
        assert str(language) == expected_result_of_method_str

    def test_values_of_record_fields(self, language_factory):
        language = language_factory(name=language_names[0])
        actual_name = language.name
        expected_name = language_names[0]
        assert actual_name, expected_name
        assert Language.objects.count() == 1


@pytest.mark.django_db
class TestDistributorModel:
    label_argvalues = [("name", "name"), ]
    label_ids = [
        f"'{arg[0]}' field: is label '{arg[1]}'?"
        for arg in label_argvalues
    ]
    field_argvalues = [
        ("name", "max_length", 32),
        ("name", "unique", True),
    ]
    field_ids = [
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?"
        for arg in field_argvalues
    ]

    def test_record_is_instance_of_model(self, distributor):
        assert isinstance(distributor, Distributor)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_argvalues,
        ids=label_ids
    )
    def test_label_of_model_field(
            self, distributor, field_name, expected_label
    ):
        actual_label = distributor._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_argvalues,
        ids=field_ids
    )
    def test_options_of_model_fields(
            self, distributor, field_name, option_name, expected_option_value
    ):
        if option_name == "max_length":
            actual_option_value = distributor._meta.get_field(field_name).max_length
        elif option_name == "unique":
            actual_option_value = distributor._meta.get_field(field_name).unique
        else:
            raise AttributeError(
                f"String '{option_name}' cannot be an attribute."
            )
        assert actual_option_value == expected_option_value

    def test_record_string_representation_is_distributor_name(
            self, distributor
    ):
        expected_result_of_method_str = distributor.name
        assert str(distributor) == expected_result_of_method_str

    def test_values_of_record_fields(self, distributor_factory):
        distributor = distributor_factory(name=distributor_names[0])
        actual_name = distributor.name
        expected_name = distributor_names[0]
        assert actual_name, expected_name
        assert Distributor.objects.count() == 1
