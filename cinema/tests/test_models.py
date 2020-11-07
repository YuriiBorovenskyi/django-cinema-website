import pytest
from datetime import date

from cinema.models import (
    Country,
    Genre,
    ImdbRating,
    MpaaRating,
    Language,
    Distributor,
    CinemaPerson,
    CinemaProfession,
    Film,
    CinemaFilmPersonProfession,
)


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

    def test_string_representation_of_record(self, country_factory):
        country = country_factory(name="UK")
        assert str(country) == "UK"


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

    def test_string_representation_of_record(self, genre_factory):
        genre = genre_factory(name="Western")
        assert str(genre) == "Western"


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

    def test_string_representation_of_record(self, imdb_rating_factory):
        imdb_rating = imdb_rating_factory(value=9.0)
        assert str(imdb_rating) == "9.0"


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

    def test_string_representation_of_record(self, mpaa_rating_factory):
        mpaa_rating = mpaa_rating_factory(
            value="PG-13", description="Children under 13"
        )
        assert str(mpaa_rating) == "PG-13"


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

    def test_string_representation_of_record(self, language_factory):
        language = language_factory(name="English")
        assert str(language) == "English"


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

    def test_string_representation_of_record(self, distributor_factory):
        distributor = distributor_factory(name="Columbia Pictures")
        assert str(distributor) == "Columbia Pictures"


@pytest.mark.django_db
class TestCinemaPersonModel:
    label_argvalues = [
        ("gender", "gender"),
        ("country", "country"),
        ("birthday", "birthday"),
        ("user", "user"),
        ("bio", "bio"),
        ("oscar_awards", "oscar awards"),
        ("avatar", "avatar"),
    ]
    label_ids = [
        f"'{arg[0]}' field: is label '{arg[1]}'?"
        for arg in label_argvalues
    ]
    field_argvalues = [
        ("gender", "max_length", 1),
        ("gender", "choices", (("M", "Male"), ("F", "Female"),)),
        ("gender", "default", "M"),
        ("country", "default", 1),
        ("birthday", "null", True),
        ("birthday", "blank", True),
        ("oscar_awards", "default", 0),
        ("avatar", "null", True),
        ("avatar", "blank", True),
    ]
    field_ids = [
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?"
        for arg in field_argvalues
    ]

    def test_record_is_instance_of_model(self, cinema_person):
        assert isinstance(cinema_person, CinemaPerson)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_argvalues,
        ids=label_ids
    )
    def test_label_of_model_field(
            self, cinema_person, field_name, expected_label
    ):
        actual_label = cinema_person._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_argvalues,
        ids=field_ids
    )
    def test_options_of_model_fields(
            self, cinema_person, field_name, option_name, expected_option_value
    ):
        if option_name == "max_length":
            actual_option_value = cinema_person._meta.get_field(
                field_name
            ).max_length
        elif option_name == "choices":
            actual_option_value = cinema_person._meta.get_field(
                field_name
            ).choices
        elif option_name == "default":
            actual_option_value = cinema_person._meta.get_field(
                field_name
            ).default
        elif option_name == "null":
            actual_option_value = cinema_person._meta.get_field(field_name).null
        elif option_name == "blank":
            actual_option_value = cinema_person._meta.get_field(
                field_name
            ).blank
        else:
            raise AttributeError(
                f"String '{option_name}' cannot be an attribute."
            )
        assert actual_option_value == expected_option_value

    def test_string_representation_of_record(
            self, user_factory, cinema_person_factory
    ):
        user = user_factory(first_name="Tom", last_name="Hanks")
        cinema_person = cinema_person_factory(user=user)
        assert str(cinema_person) == "Tom Hanks"

    def test_fullname_of_cinema_person(
            self, user_factory, cinema_person_factory
    ):
        user = user_factory(first_name="Tom", last_name="Hanks")
        cinema_person = cinema_person_factory(user=user)
        assert cinema_person.fullname == "Tom Hanks"

    def test_age_of_cinema_person(self, cinema_person_factory):
        cinema_person = cinema_person_factory(
            birthday=date(year=1956, month=7, day=9)
        )
        assert cinema_person.age == 64


@pytest.mark.django_db
class TestCinemaProfessionModel:
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

    def test_record_is_instance_of_model(self, cinema_profession):
        assert isinstance(cinema_profession, CinemaProfession)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_argvalues,
        ids=label_ids
    )
    def test_label_of_model_field(
            self, cinema_profession, field_name, expected_label
    ):
        actual_label = cinema_profession._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_argvalues,
        ids=field_ids
    )
    def test_options_of_model_fields(
            self, cinema_profession, field_name, option_name,
            expected_option_value
    ):
        if option_name == "max_length":
            actual_option_value = cinema_profession._meta.get_field(
                field_name
            ).max_length
        elif option_name == "unique":
            actual_option_value = cinema_profession._meta.get_field(
                field_name
            ).unique
        else:
            raise AttributeError(
                f"String '{option_name}' cannot be an attribute."
            )
        assert actual_option_value == expected_option_value

    def test_string_representation_of_record(self, cinema_profession_factory):
        cinema_profession = cinema_profession_factory(name="Actor")
        assert str(cinema_profession) == "Actor"


@pytest.mark.django_db
class TestFilmModel:
    label_argvalues = [
        ("title", "title"),
        ("country", "country"),
        ("genre", "genre"),
        ("staff", "staff"),
        ("budget", "budget"),
        ("usa_gross", "usa gross"),
        ("world_gross", "world gross"),
        ("run_time", "run time"),
        ("description", "description"),
        ("release_data", "release data"),
        ("language", "language"),
        ("distributor", "distributor"),
        ("imdb_rating", "imdb rating"),
        ("mpaa_rating", "mpaa rating"),
        ("oscar_awards", "oscar awards"),
        ("poster", "poster"),
    ]
    label_ids = [
        f"'{arg[0]}' field: is label '{arg[1]}'?"
        for arg in label_argvalues
    ]
    field_argvalues = [
        ("title", "max_length", 64),
        ("title", "db_index", True),
        ("budget", "null", True),
        ("budget", "blank", True),
        ("usa_gross", "default", 0),
        ("world_gross", "default", 0),
        ("mpaa_rating", "default", 1),
        ("oscar_awards", "default", 0),
        ("poster", "blank", True),
        ("poster", "null", True),
    ]
    field_ids = [
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?"
        for arg in field_argvalues
    ]

    def test_record_is_instance_of_model(self, film_fixture):
        assert isinstance(film_fixture, Film)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_argvalues,
        ids=label_ids
    )
    def test_label_of_model_field(
            self, film_fixture, field_name, expected_label
    ):
        actual_label = film_fixture._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_argvalues,
        ids=field_ids
    )
    def test_options_of_model_fields(
            self, film_fixture, field_name, option_name, expected_option_value
    ):
        if option_name == "max_length":
            actual_option_value = film_fixture._meta.get_field(
                field_name
            ).max_length
        elif option_name == "db_index":
            actual_option_value = film_fixture._meta.get_field(
                field_name
            ).db_index
        elif option_name == "default":
            actual_option_value = film_fixture._meta.get_field(
                field_name
            ).default
        elif option_name == "null":
            actual_option_value = film_fixture._meta.get_field(field_name).null
        elif option_name == "blank":
            actual_option_value = film_fixture._meta.get_field(
                field_name
            ).blank
        else:
            raise AttributeError(
                f"String '{option_name}' cannot be an attribute."
            )
        assert actual_option_value == expected_option_value

    def test_string_representation_of_record(self, film_fixture):
        film_fixture.title = "Forrest Gump"
        assert str(film_fixture) == "Forrest Gump"

    def test_year_of_film(self, film_fixture):
        film_fixture.release_data = date(year=2002, month=7, day=9)
        assert film_fixture.year == 2002


@pytest.mark.django_db
class TestCinemaFilmPersonProfessionModel:
    label_argvalues = [
        ("cinema_person", "cinema person"),
        ("film", "film"),
        ("profession", "profession"),
    ]
    label_ids = [
        f"'{arg[0]}' field: is label '{arg[1]}'?"
        for arg in label_argvalues
    ]
    field_argvalues = [("profession", "default", 2), ]
    field_ids = [
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?"
        for arg in field_argvalues
    ]

    def test_record_is_instance_of_model(self, cinema_film_person_profession):
        assert isinstance(
            cinema_film_person_profession, CinemaFilmPersonProfession
        )

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_argvalues,
        ids=label_ids
    )
    def test_label_of_model_field(
            self, cinema_film_person_profession, field_name, expected_label
    ):
        actual_label = cinema_film_person_profession._meta.get_field(
            field_name
        ).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_argvalues,
        ids=field_ids
    )
    def test_options_of_model_fields(
            self, cinema_film_person_profession, field_name, option_name,
            expected_option_value
    ):
        if option_name == "default":
            actual_option_value = cinema_film_person_profession._meta.get_field(
                field_name
            ).default
        else:
            raise AttributeError(
                f"String '{option_name}' cannot be an attribute."
            )
        assert actual_option_value == expected_option_value

    def test_string_representation_of_record(
            self, cinema_film_person_profession
    ):
        cinema_film_person_profession.film.title = "Forrest Gump"
        cinema_film_person_profession.profession.name = "Actor"
        cinema_film_person_profession.cinema_person.user.first_name = "Tom"
        cinema_film_person_profession.cinema_person.user.last_name = "Hanks"

        assert str(
            cinema_film_person_profession
        ) == "Forrest Gump: Actor - Tom Hanks"













# @pytest.mark.django_db
# class TestCinemaPersonManager:
#     def test_get_brief_data(self, cinema_person_factory):
#         cp_1 = cinema_person_factory()
#         cp_2 = cinema_person_factory()
#         expected_data = [
#             {'pk': cp_2.pk, 'user__first_name': cp_2.user.first_name,
#              'user__last_name': cp_2.user.last_name},
#             {'pk': cp_1.pk, 'user__first_name': cp_1.user.first_name,
#              'user__last_name': cp_1.user.last_name},
#         ]
#         result = CinemaPerson.persons.get_brief_data()
#         assert len(result) == 2
#         assert expected_data == list(map(lambda x: x._asdict(), result))
