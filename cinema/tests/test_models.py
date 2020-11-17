from datetime import date

import pytest

from cinema.models import (
    CinemaFilmPersonProfession,
    CinemaPerson,
    CinemaProfession,
    CommentToFilm,
    CommentToNews,
    CommentToPerson,
    CommentToProduct,
    Country,
    Distributor,
    Film,
    Genre,
    ImdbRating,
    Language,
    MpaaRating,
    News,
    Product,
    upload_photo_to_news_detail,
    upload_photo_to_news_feed,
    upload_to_cinema_person,
    upload_to_film,
)


@pytest.mark.django_db
class TestCountryModel:
    label_arg_values = (("name", "name"),)
    label_ids = (
        f"'{arg[0]}' field: is label '{arg[1]}'?" for arg in label_arg_values
    )
    field_arg_values = (
        ("name", "max_length", 64),
        ("name", "unique", True),
    )
    field_ids = (
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?" for arg in field_arg_values
    )

    def test_record_is_instance_of_model_class(self, country):
        assert isinstance(country, Country)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_arg_values,
        ids=label_ids,
    )
    def test_labels_of_model_fields(
        self,
        country,
        field_name,
        expected_label,
    ):
        actual_label = country._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_arg_values,
        ids=field_ids,
    )
    def test_options_of_model_fields(
        self,
        country,
        field_name,
        option_name,
        expected_option_value,
    ):
        if option_name == "max_length":
            actual_option_value = country._meta.get_field(field_name).max_length
        else:
            actual_option_value = country._meta.get_field(field_name).unique

        assert actual_option_value == expected_option_value

    def test_model_ordering(self, country):
        assert country._meta.ordering == ["name"]

    def test_string_representation_of_record(self, country_factory):
        country = country_factory(name="UK")
        assert str(country) == "UK"


@pytest.mark.django_db
class TestGenreModel:
    label_arg_values = (("name", "name"),)
    label_ids = (
        f"'{arg[0]}' field: is label '{arg[1]}'?" for arg in label_arg_values
    )
    field_arg_values = (
        ("name", "max_length", 16),
        ("name", "unique", True),
    )
    field_ids = (
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?" for arg in field_arg_values
    )

    def test_record_is_instance_of_model_class(self, genre):
        assert isinstance(genre, Genre)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_arg_values,
        ids=label_ids,
    )
    def test_labels_of_model_fields(
        self,
        genre,
        field_name,
        expected_label,
    ):
        actual_label = genre._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_arg_values,
        ids=field_ids,
    )
    def test_options_of_model_fields(
        self,
        genre,
        field_name,
        option_name,
        expected_option_value,
    ):
        if option_name == "max_length":
            actual_option_value = genre._meta.get_field(field_name).max_length
        else:
            actual_option_value = genre._meta.get_field(field_name).unique

        assert actual_option_value == expected_option_value

    def test_model_ordering(self, genre):
        assert genre._meta.ordering == ["name"]

    def test_string_representation_of_record(self, genre_factory):
        genre = genre_factory(name="Western")
        assert str(genre) == "Western"


@pytest.mark.django_db
class TestImdbRatingModel:
    label_arg_values = (("value", "value"),)
    label_ids = (
        f"'{arg[0]}' field: is label '{arg[1]}'?" for arg in label_arg_values
    )
    field_arg_values = (
        ("value", "max_digits", 2),
        ("value", "decimal_places", 1),
        ("value", "unique", True),
    )
    field_ids = (
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?" for arg in field_arg_values
    )

    def test_record_is_instance_of_model_class(self, imdb_rating):
        assert isinstance(imdb_rating, ImdbRating)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_arg_values,
        ids=label_ids,
    )
    def test_labels_of_model_fields(
        self,
        imdb_rating,
        field_name,
        expected_label,
    ):
        actual_label = imdb_rating._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_arg_values,
        ids=field_ids,
    )
    def test_options_of_model_fields(
        self,
        imdb_rating,
        field_name,
        option_name,
        expected_option_value,
    ):
        if option_name == "max_digits":
            actual_option_value = imdb_rating._meta.get_field(
                field_name,
            ).max_digits
        elif option_name == "decimal_places":
            actual_option_value = imdb_rating._meta.get_field(
                field_name,
            ).decimal_places
        else:
            actual_option_value = imdb_rating._meta.get_field(field_name).unique

        assert actual_option_value == expected_option_value

    def test_model_ordering(self, imdb_rating):
        assert imdb_rating._meta.ordering == ["value"]

    def test_string_representation_of_record(self, imdb_rating_factory):
        imdb_rating = imdb_rating_factory(value=9.0)
        assert str(imdb_rating) == "9.0"


@pytest.mark.django_db
class TestMpaaRatingModel:
    label_arg_values = (
        ("value", "value"),
        ("description", "description"),
    )
    label_ids = (
        f"'{arg[0]}' field: is label '{arg[1]}'?" for arg in label_arg_values
    )
    field_arg_values = (
        ("value", "max_length", 10),
        ("value", "unique", True),
        ("description", "max_length", 512),
        ("description", "unique", True),
    )
    field_ids = (
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?" for arg in field_arg_values
    )

    def test_record_is_instance_of_model_class(self, mpaa_rating):
        assert isinstance(mpaa_rating, MpaaRating)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_arg_values,
        ids=label_ids,
    )
    def test_labels_of_model_fields(
        self,
        mpaa_rating,
        field_name,
        expected_label,
    ):
        actual_label = mpaa_rating._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_arg_values,
        ids=field_ids,
    )
    def test_options_of_model_fields(
        self,
        mpaa_rating,
        field_name,
        option_name,
        expected_option_value,
    ):
        if option_name == "max_length":
            actual_option_value = mpaa_rating._meta.get_field(
                field_name,
            ).max_length
        else:
            actual_option_value = mpaa_rating._meta.get_field(field_name).unique

        assert actual_option_value == expected_option_value

    def test_model_ordering(self, mpaa_rating):
        assert mpaa_rating._meta.ordering == ["value"]

    def test_string_representation_of_record(self, mpaa_rating_factory):
        mpaa_rating = mpaa_rating_factory(
            value="PG-13",
            description="Children under 13",
        )
        assert str(mpaa_rating) == "PG-13"


@pytest.mark.django_db
class TestLanguageModel:
    label_arg_values = (("name", "name"),)
    label_ids = (
        f"'{arg[0]}' field: is label '{arg[1]}'?" for arg in label_arg_values
    )
    field_arg_values = (
        ("name", "max_length", 16),
        ("name", "unique", True),
    )
    field_ids = (
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?" for arg in field_arg_values
    )

    def test_record_is_instance_of_model_class(self, language):
        assert isinstance(language, Language)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_arg_values,
        ids=label_ids,
    )
    def test_labels_of_model_fields(
        self,
        language,
        field_name,
        expected_label,
    ):
        actual_label = language._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_arg_values,
        ids=field_ids,
    )
    def test_options_of_model_fields(
        self,
        language,
        field_name,
        option_name,
        expected_option_value,
    ):
        if option_name == "max_length":
            actual_option_value = language._meta.get_field(
                field_name,
            ).max_length
        else:
            actual_option_value = language._meta.get_field(field_name).unique

        assert actual_option_value == expected_option_value

    def test_model_ordering(self, language):
        assert language._meta.ordering == ["name"]

    def test_string_representation_of_record(self, language_factory):
        language = language_factory(name="English")
        assert str(language) == "English"


@pytest.mark.django_db
class TestDistributorModel:
    label_arg_values = (("name", "name"),)
    label_ids = (
        f"'{arg[0]}' field: is label '{arg[1]}'?" for arg in label_arg_values
    )
    field_arg_values = (
        ("name", "max_length", 32),
        ("name", "unique", True),
    )
    field_ids = (
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?" for arg in field_arg_values
    )

    def test_record_is_instance_of_model_class(self, distributor):
        assert isinstance(distributor, Distributor)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_arg_values,
        ids=label_ids,
    )
    def test_labels_of_model_fields(
        self,
        distributor,
        field_name,
        expected_label,
    ):
        actual_label = distributor._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_arg_values,
        ids=field_ids,
    )
    def test_options_of_model_fields(
        self,
        distributor,
        field_name,
        option_name,
        expected_option_value,
    ):
        if option_name == "max_length":
            actual_option_value = distributor._meta.get_field(
                field_name,
            ).max_length
        else:
            actual_option_value = distributor._meta.get_field(field_name).unique

        assert actual_option_value == expected_option_value

    def test_model_ordering(self, distributor):
        assert distributor._meta.ordering == ["name"]

    def test_string_representation_of_record(self, distributor_factory):
        distributor = distributor_factory(name="Columbia Pictures")
        assert str(distributor) == "Columbia Pictures"


@pytest.mark.django_db
class TestCinemaPersonModel:
    label_arg_values = (
        ("gender", "gender"),
        ("country", "country"),
        ("birthday", "birthday"),
        ("user", "user"),
        ("bio", "bio"),
        ("oscar_awards", "oscar awards"),
        ("avatar", "avatar"),
    )
    label_ids = (
        f"'{arg[0]}' field: is label '{arg[1]}'?" for arg in label_arg_values
    )
    field_arg_values = (
        ("gender", "max_length", 1),
        ("gender", "choices", (("M", "Male"), ("F", "Female"))),
        ("gender", "default", "M"),
        ("country", "default", 1),
        ("birthday", "null", True),
        ("birthday", "blank", True),
        ("oscar_awards", "default", 0),
        ("avatar", "null", True),
        ("avatar", "blank", True),
    )
    field_ids = (
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?" for arg in field_arg_values
    )

    def test_record_is_instance_of_model_class(self, cinema_person):
        assert isinstance(cinema_person, CinemaPerson)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_arg_values,
        ids=label_ids,
    )
    def test_labels_of_model_fields(
        self,
        cinema_person,
        field_name,
        expected_label,
    ):
        actual_label = cinema_person._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_arg_values,
        ids=field_ids,
    )
    def test_options_of_model_fields(
        self,
        cinema_person,
        field_name,
        option_name,
        expected_option_value,
    ):
        if option_name == "max_length":
            actual_option_value = cinema_person._meta.get_field(
                field_name,
            ).max_length
        elif option_name == "choices":
            actual_option_value = cinema_person._meta.get_field(
                field_name,
            ).choices
        elif option_name == "default":
            actual_option_value = cinema_person._meta.get_field(
                field_name,
            ).default
        elif option_name == "null":
            actual_option_value = cinema_person._meta.get_field(field_name).null
        else:
            actual_option_value = cinema_person._meta.get_field(
                field_name,
            ).blank

        assert actual_option_value == expected_option_value

    def test_model_ordering(self, cinema_person):
        assert cinema_person._meta.ordering == [
            "user__first_name",
            "user__last_name",
        ]

    def test_string_representation_of_record(
        self,
        user_factory,
        cinema_person_factory,
    ):
        user = user_factory(first_name="Tom", last_name="Hanks")
        cinema_person = cinema_person_factory(user=user)
        assert str(cinema_person) == "Tom Hanks"

    def test_fullname_of_cinema_person(
        self,
        user_factory,
        cinema_person_factory,
    ):
        user = user_factory(first_name="Tom", last_name="Hanks")
        cinema_person = cinema_person_factory(user=user)
        assert cinema_person.fullname == "Tom Hanks"

    def test_age_of_cinema_person(self, cinema_person_factory):
        cinema_person = cinema_person_factory(
            birthday=date(year=1956, month=7, day=9),
        )
        assert cinema_person.age == 64

    def test_upload_to_cinema_person(self, cinema_person_factory):
        person = cinema_person_factory()
        expected_data = (
            f"cinema_persons/{person.user.first_name}"
            f"_{person.user.last_name}_{person.pk}.jpg"
        )
        assert upload_to_cinema_person(person, "") == expected_data


@pytest.mark.django_db
class TestCinemaProfessionModel:
    label_arg_values = (("name", "name"),)
    label_ids = (
        f"'{arg[0]}' field: is label '{arg[1]}'?" for arg in label_arg_values
    )
    field_arg_values = (
        ("name", "max_length", 16),
        ("name", "unique", True),
    )
    field_ids = (
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?" for arg in field_arg_values
    )

    def test_record_is_instance_of_model_class(self, cinema_profession):
        assert isinstance(cinema_profession, CinemaProfession)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_arg_values,
        ids=label_ids,
    )
    def test_labels_of_model_fields(
        self,
        cinema_profession,
        field_name,
        expected_label,
    ):
        actual_label = cinema_profession._meta.get_field(
            field_name,
        ).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_arg_values,
        ids=field_ids,
    )
    def test_options_of_model_fields(
        self,
        cinema_profession,
        field_name,
        option_name,
        expected_option_value,
    ):
        if option_name == "max_length":
            actual_option_value = cinema_profession._meta.get_field(
                field_name,
            ).max_length
        else:
            actual_option_value = cinema_profession._meta.get_field(
                field_name,
            ).unique

        assert actual_option_value == expected_option_value

    def test_model_ordering(self, cinema_profession):
        assert cinema_profession._meta.ordering == ["pk"]

    def test_string_representation_of_record(self, cinema_profession_factory):
        cinema_profession = cinema_profession_factory(name="Actor")
        assert str(cinema_profession) == "Actor"


@pytest.mark.django_db
class TestFilmModel:
    label_arg_values = (
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
    )
    label_ids = (
        f"'{arg[0]}' field: is label '{arg[1]}'?" for arg in label_arg_values
    )
    field_arg_values = (
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
    )
    field_ids = (
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?" for arg in field_arg_values
    )

    def test_record_is_instance_of_model_class(self, film_fixture):
        assert isinstance(film_fixture, Film)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_arg_values,
        ids=label_ids,
    )
    def test_labels_of_model_fields(
        self,
        film_fixture,
        field_name,
        expected_label,
    ):
        actual_label = film_fixture._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_arg_values,
        ids=field_ids,
    )
    def test_options_of_model_fields(
        self,
        film_fixture,
        field_name,
        option_name,
        expected_option_value,
    ):
        if option_name == "max_length":
            actual_option_value = film_fixture._meta.get_field(
                field_name,
            ).max_length
        elif option_name == "db_index":
            actual_option_value = film_fixture._meta.get_field(
                field_name,
            ).db_index
        elif option_name == "default":
            actual_option_value = film_fixture._meta.get_field(
                field_name,
            ).default
        elif option_name == "null":
            actual_option_value = film_fixture._meta.get_field(field_name).null
        else:
            actual_option_value = film_fixture._meta.get_field(
                field_name,
            ).blank

        assert actual_option_value == expected_option_value

    def test_model_ordering(self, film_fixture):
        assert film_fixture._meta.ordering == ["title"]

    def test_string_representation_of_record(self, film_fixture):
        film_fixture.title = "Forrest Gump"
        assert str(film_fixture) == "Forrest Gump"

    def test_year_of_film(self, film_fixture):
        film_fixture.release_data = date(year=2002, month=7, day=9)
        assert film_fixture.year == 2002

    def test_upload_to_film(self, film_factory):
        film = film_factory()
        expected_data = f"films/{film.title}_{film.pk}.jpg"
        assert upload_to_film(film, "") == expected_data


@pytest.mark.django_db
class TestCinemaFilmPersonProfessionModel:
    label_arg_values = (
        ("cinema_person", "cinema person"),
        ("film", "film"),
        ("profession", "profession"),
    )
    label_ids = (
        f"'{arg[0]}' field: is label '{arg[1]}'?" for arg in label_arg_values
    )
    field_arg_values = (("profession", "default", 2),)
    field_ids = (
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?" for arg in field_arg_values
    )

    def test_record_is_instance_of_model_class(
        self,
        cinema_film_person_profession,
    ):
        assert isinstance(
            cinema_film_person_profession,
            CinemaFilmPersonProfession,
        )

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_arg_values,
        ids=label_ids,
    )
    def test_labels_of_model_fields(
        self,
        cinema_film_person_profession,
        field_name,
        expected_label,
    ):
        actual_label = cinema_film_person_profession._meta.get_field(
            field_name,
        ).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_arg_values,
        ids=field_ids,
    )
    def test_options_of_model_fields(
        self,
        cinema_film_person_profession,
        field_name,
        option_name,
        expected_option_value,
    ):
        actual_option_value = cinema_film_person_profession._meta.get_field(
            field_name,
        ).default
        assert actual_option_value == expected_option_value

    def test_model_ordering(self, cinema_film_person_profession):
        assert cinema_film_person_profession._meta.ordering == [
            "film__title",
            "profession",
            "cinema_person__user__first_name",
        ]

    def test_string_representation_of_record(
        self,
        cinema_film_person_profession,
    ):
        cinema_film_person_profession.film.title = "Forrest Gump"
        cinema_film_person_profession.profession.name = "Actor"
        cinema_film_person_profession.cinema_person.user.first_name = "Tom"
        cinema_film_person_profession.cinema_person.user.last_name = "Hanks"

        assert (
            str(
                cinema_film_person_profession,
            )
            == "Forrest Gump: Actor - Tom Hanks"
        )


@pytest.mark.django_db
class TestNewsModel:
    label_arg_values = (
        ("title", "title"),
        ("description", "description"),
        ("news_source", "news source"),
        ("news_author", "news author"),
        ("film", "film"),
        ("cinema_person", "cinema person"),
        ("news_feed_photo", "news feed photo"),
        ("news_detail_photo", "news detail photo"),
        ("created_at", "created at"),
    )
    label_ids = (
        f"'{arg[0]}' field: is label '{arg[1]}'?" for arg in label_arg_values
    )
    field_arg_values = (
        ("title", "max_length", 128),
        ("title", "unique", True),
        ("news_source", "max_length", 32),
        ("news_author", "max_length", 64),
        ("film", "blank", True),
        ("cinema_person", "blank", True),
        ("news_feed_photo", "blank", True),
        ("news_feed_photo", "null", True),
        ("news_detail_photo", "blank", True),
        ("news_detail_photo", "null", True),
        ("created_at", "auto_now", True),
        ("created_at", "db_index", True),
    )
    field_ids = (
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?" for arg in field_arg_values
    )

    def test_record_is_instance_of_model_class(self, news):
        assert isinstance(news, News)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_arg_values,
        ids=label_ids,
    )
    def test_labels_of_model_fields(
        self,
        news,
        field_name,
        expected_label,
    ):
        actual_label = news._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_arg_values,
        ids=field_ids,
    )
    def test_options_of_model_fields(
        self,
        news,
        field_name,
        option_name,
        expected_option_value,
    ):
        if option_name == "max_length":
            actual_option_value = news._meta.get_field(
                field_name,
            ).max_length
        elif option_name == "db_index":
            actual_option_value = news._meta.get_field(
                field_name,
            ).db_index
        elif option_name == "unique":
            actual_option_value = news._meta.get_field(
                field_name,
            ).unique
        elif option_name == "null":
            actual_option_value = news._meta.get_field(field_name).null
        elif option_name == "blank":
            actual_option_value = news._meta.get_field(
                field_name,
            ).blank
        else:
            actual_option_value = news._meta.get_field(
                field_name,
            ).auto_now

        assert actual_option_value == expected_option_value

    def test_model_ordering(self, news):
        assert news._meta.ordering == ["-created_at"]

    def test_string_representation_of_record(self, news):
        news.title = "Forrest Gump"
        assert str(news) == "Forrest Gump"

    def test_upload_photo_to_news_feed(self, news_factory):
        news = news_factory()
        expected_data = f"cinema_news_feed/{news.title}_{news.pk}.jpg"
        assert upload_photo_to_news_feed(news, "") == expected_data

    def test_upload_photo_to_news_detail(self, news_factory):
        news = news_factory()
        expected_data = f"cinema_news_detail/{news.title}_{news.pk}.jpg"
        assert upload_photo_to_news_detail(news, "") == expected_data


@pytest.mark.django_db
class TestProductModel:
    label_arg_values = (
        ("price", "price"),
        ("in_stock", "in stock"),
        ("film", "film"),
        ("created_at", "created at"),
    )
    label_ids = (
        f"'{arg[0]}' field: is label '{arg[1]}'?" for arg in label_arg_values
    )
    field_arg_values = (
        ("price", "max_digits", 5),
        ("price", "decimal_places", 2),
        ("in_stock", "default", 0),
        ("created_at", "auto_now", True),
        ("created_at", "db_index", True),
    )
    field_ids = (
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?" for arg in field_arg_values
    )

    def test_record_is_instance_of_model_class(self, product):
        assert isinstance(product, Product)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_arg_values,
        ids=label_ids,
    )
    def test_labels_of_model_fields(
        self,
        product,
        field_name,
        expected_label,
    ):
        actual_label = product._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_arg_values,
        ids=field_ids,
    )
    def test_options_of_model_fields(
        self,
        product,
        field_name,
        option_name,
        expected_option_value,
    ):
        if option_name == "max_digits":
            actual_option_value = product._meta.get_field(
                field_name,
            ).max_digits
        elif option_name == "decimal_places":
            actual_option_value = product._meta.get_field(
                field_name,
            ).decimal_places
        elif option_name == "default":
            actual_option_value = product._meta.get_field(
                field_name,
            ).default
        elif option_name == "auto_now":
            actual_option_value = product._meta.get_field(
                field_name,
            ).auto_now
        else:
            actual_option_value = product._meta.get_field(
                field_name,
            ).db_index

        assert actual_option_value == expected_option_value

    def test_model_ordering(self, product):
        assert product._meta.ordering == ["film__title"]

    def test_string_representation_of_record(self, product_factory):
        product = product_factory(film__title="Forrest Gump")
        assert str(product) == "Forrest Gump [Blu-ray]"


@pytest.mark.django_db
class TestCommentToPersonModel:
    label_arg_values = (
        ("author", "author"),
        ("content", "content"),
        ("is_active", "Display on screen?"),
        ("created_at", "created at"),
        ("cinema_person", "cinema person"),
    )
    label_ids = (
        f"'{arg[0]}' field: is label '{arg[1]}'?" for arg in label_arg_values
    )
    field_arg_values = (
        ("author", "max_length", 32),
        ("is_active", "default", True),
        ("is_active", "db_index", True),
        ("is_active", "verbose_name", "Display on screen?"),
        ("created_at", "auto_now", True),
        ("created_at", "db_index", True),
    )
    field_ids = (
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?" for arg in field_arg_values
    )

    def test_record_is_instance_of_model_class(self, comment_to_person):
        assert isinstance(comment_to_person, CommentToPerson)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_arg_values,
        ids=label_ids,
    )
    def test_labels_of_model_fields(
        self,
        comment_to_person,
        field_name,
        expected_label,
    ):
        actual_label = comment_to_person._meta.get_field(
            field_name,
        ).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_arg_values,
        ids=field_ids,
    )
    def test_options_of_model_fields(
        self,
        comment_to_person,
        field_name,
        option_name,
        expected_option_value,
    ):
        if option_name == "max_length":
            actual_option_value = comment_to_person._meta.get_field(
                field_name,
            ).max_length
        elif option_name == "max_digits":
            actual_option_value = comment_to_person._meta.get_field(
                field_name,
            ).max_digits
        elif option_name == "default":
            actual_option_value = comment_to_person._meta.get_field(
                field_name,
            ).default
        elif option_name == "auto_now":
            actual_option_value = comment_to_person._meta.get_field(
                field_name,
            ).auto_now
        elif option_name == "db_index":
            actual_option_value = comment_to_person._meta.get_field(
                field_name,
            ).db_index
        else:
            actual_option_value = comment_to_person._meta.get_field(
                field_name,
            ).verbose_name

        assert actual_option_value == expected_option_value

    def test_model_ordering(self, comment_to_person):
        assert comment_to_person._meta.ordering == ["-created_at"]


@pytest.mark.django_db
class TestCommentToFilmModel:
    label_arg_values = (
        ("author", "author"),
        ("content", "content"),
        ("is_active", "Display on screen?"),
        ("created_at", "created at"),
        ("film", "film"),
    )
    label_ids = (
        f"'{arg[0]}' field: is label '{arg[1]}'?" for arg in label_arg_values
    )
    field_arg_values = (
        ("author", "max_length", 32),
        ("is_active", "default", True),
        ("is_active", "db_index", True),
        ("is_active", "verbose_name", "Display on screen?"),
        ("created_at", "auto_now", True),
        ("created_at", "db_index", True),
    )
    field_ids = (
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?" for arg in field_arg_values
    )

    def test_record_is_instance_of_model_class(self, comment_to_film):
        assert isinstance(comment_to_film, CommentToFilm)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_arg_values,
        ids=label_ids,
    )
    def test_labels_of_model_fields(
        self,
        comment_to_film,
        field_name,
        expected_label,
    ):
        actual_label = comment_to_film._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_arg_values,
        ids=field_ids,
    )
    def test_options_of_model_fields(
        self,
        comment_to_film,
        field_name,
        option_name,
        expected_option_value,
    ):
        if option_name == "max_length":
            actual_option_value = comment_to_film._meta.get_field(
                field_name,
            ).max_length
        elif option_name == "max_digits":
            actual_option_value = comment_to_film._meta.get_field(
                field_name,
            ).max_digits
        elif option_name == "default":
            actual_option_value = comment_to_film._meta.get_field(
                field_name,
            ).default
        elif option_name == "auto_now":
            actual_option_value = comment_to_film._meta.get_field(
                field_name,
            ).auto_now
        elif option_name == "db_index":
            actual_option_value = comment_to_film._meta.get_field(
                field_name,
            ).db_index
        else:
            actual_option_value = comment_to_film._meta.get_field(
                field_name,
            ).verbose_name

        assert actual_option_value == expected_option_value

    def test_model_ordering(self, comment_to_film):
        assert comment_to_film._meta.ordering == ["-created_at"]


@pytest.mark.django_db
class TestCommentToNewsModel:
    label_arg_values = (
        ("author", "author"),
        ("content", "content"),
        ("is_active", "Display on screen?"),
        ("created_at", "created at"),
        ("news", "news"),
    )
    label_ids = (
        f"'{arg[0]}' field: is label '{arg[1]}'?" for arg in label_arg_values
    )
    field_arg_values = (
        ("author", "max_length", 32),
        ("is_active", "default", True),
        ("is_active", "db_index", True),
        ("is_active", "verbose_name", "Display on screen?"),
        ("created_at", "auto_now", True),
        ("created_at", "db_index", True),
    )
    field_ids = (
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?" for arg in field_arg_values
    )

    def test_record_is_instance_of_model_class(self, comment_to_news):
        assert isinstance(comment_to_news, CommentToNews)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_arg_values,
        ids=label_ids,
    )
    def test_labels_of_model_fields(
        self,
        comment_to_news,
        field_name,
        expected_label,
    ):
        actual_label = comment_to_news._meta.get_field(field_name).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_arg_values,
        ids=field_ids,
    )
    def test_options_of_model_fields(
        self,
        comment_to_news,
        field_name,
        option_name,
        expected_option_value,
    ):
        if option_name == "max_length":
            actual_option_value = comment_to_news._meta.get_field(
                field_name,
            ).max_length
        elif option_name == "max_digits":
            actual_option_value = comment_to_news._meta.get_field(
                field_name,
            ).max_digits
        elif option_name == "default":
            actual_option_value = comment_to_news._meta.get_field(
                field_name,
            ).default
        elif option_name == "auto_now":
            actual_option_value = comment_to_news._meta.get_field(
                field_name,
            ).auto_now
        elif option_name == "db_index":
            actual_option_value = comment_to_news._meta.get_field(
                field_name,
            ).db_index
        else:
            actual_option_value = comment_to_news._meta.get_field(
                field_name,
            ).verbose_name

        assert actual_option_value == expected_option_value

    def test_model_ordering(self, comment_to_news):
        assert comment_to_news._meta.ordering == ["-created_at"]


@pytest.mark.django_db
class TestCommentToProductModel:
    label_arg_values = (
        ("author", "author"),
        ("content", "content"),
        ("is_active", "Display on screen?"),
        ("created_at", "created at"),
        ("product", "product"),
    )
    label_ids = (
        f"'{arg[0]}' field: is label '{arg[1]}'?" for arg in label_arg_values
    )
    field_arg_values = (
        ("author", "max_length", 32),
        ("is_active", "default", True),
        ("is_active", "db_index", True),
        ("is_active", "verbose_name", "Display on screen?"),
        ("created_at", "auto_now", True),
        ("created_at", "db_index", True),
    )
    field_ids = (
        f"'{arg[0]}' field: is {arg[1]} {arg[2]}?" for arg in field_arg_values
    )

    def test_record_is_instance_of_model_class(self, comment_to_product):
        assert isinstance(comment_to_product, CommentToProduct)

    @pytest.mark.parametrize(
        "field_name, expected_label",
        label_arg_values,
        ids=label_ids,
    )
    def test_labels_of_model_fields(
        self,
        comment_to_product,
        field_name,
        expected_label,
    ):
        actual_label = comment_to_product._meta.get_field(
            field_name,
        ).verbose_name
        assert actual_label == expected_label

    @pytest.mark.parametrize(
        "field_name, option_name, expected_option_value",
        field_arg_values,
        ids=field_ids,
    )
    def test_options_of_model_fields(
        self,
        comment_to_product,
        field_name,
        option_name,
        expected_option_value,
    ):
        if option_name == "max_length":
            actual_option_value = comment_to_product._meta.get_field(
                field_name,
            ).max_length
        elif option_name == "max_digits":
            actual_option_value = comment_to_product._meta.get_field(
                field_name,
            ).max_digits
        elif option_name == "default":
            actual_option_value = comment_to_product._meta.get_field(
                field_name,
            ).default
        elif option_name == "auto_now":
            actual_option_value = comment_to_product._meta.get_field(
                field_name,
            ).auto_now
        elif option_name == "db_index":
            actual_option_value = comment_to_product._meta.get_field(
                field_name,
            ).db_index
        else:
            actual_option_value = comment_to_product._meta.get_field(
                field_name,
            ).verbose_name

        assert actual_option_value == expected_option_value

    def test_model_ordering(self, comment_to_product):
        assert comment_to_product._meta.ordering == ["-created_at"]
