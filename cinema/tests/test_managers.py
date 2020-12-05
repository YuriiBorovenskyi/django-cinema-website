from datetime import date

import pytest

from cinema.models import (
    CinemaFilmPersonProfession,
    CinemaPerson,
    Film,
    News,
    Product,
)


@pytest.mark.django_db
class TestCinemaPersonManager:
    def test_get_brief_data(self, cinema_person_factory):
        person_1 = cinema_person_factory()
        person_2 = cinema_person_factory()
        expected_data = [
            {
                "pk": person_1.pk,
                "user__first_name": person_1.user.first_name,
                "user__last_name": person_1.user.last_name,
            },
            {
                "pk": person_2.pk,
                "user__first_name": person_2.user.first_name,
                "user__last_name": person_2.user.last_name,
            },
        ]
        result = CinemaPerson.persons.get_brief_data().order_by("pk")

        assert len(result) == 2
        assert expected_data == list(map(lambda x: x._asdict(), result))

    def test_filter_by_search_word(self, cinema_person_factory):
        search_word = "Tom"
        cinema_person_factory(
            user__first_name="Tom",
            user__last_name="Hanks",
        )
        cinema_person_factory(
            user__first_name="Al",
            user__last_name="Pacino",
        )
        cinema_person_factory(
            user__first_name="Tom",
            user__last_name="Cruise",
        )
        result = CinemaPerson.persons.filter_by_search_word(search_word)

        assert len(result) == 2

        for item in result:
            assert search_word in item.fullname

    def test_get_related_data(
        self,
        cinema_film_person_profession_factory,
        cinema_person_factory,
        news_factory,
        film_factory,
        genre_factory,
        cinema_profession_factory,
    ):
        person = cinema_person_factory()
        profession = cinema_profession_factory()
        genre = genre_factory()
        film = film_factory(genre=(genre,))
        cinema_film_person_profession_factory(
            cinema_person=person,
            film=film,
            profession=profession,
        )
        news = news_factory(cinema_person=(person,), film=(film,))
        expected_data = [
            {
                "pk": person.pk,
                "film__genre__name": genre.name,
                "news__pk": news.pk,
                "news__title": news.title,
            },
        ]
        result = CinemaPerson.persons.get_related_data(
            ("film__genre__name", "news__pk"),
        )

        assert len(result) == 1
        assert expected_data == list(map(lambda x: x._asdict(), result))


@pytest.mark.django_db
class TestFilmManager:
    def test_get_brief_data(self, film_factory):
        film_1 = film_factory()
        film_2 = film_factory()
        expected_data = [
            {"pk": film_1.pk, "title": film_1.title},
            {"pk": film_2.pk, "title": film_2.title},
        ]
        result = Film.films.get_brief_data().order_by("pk")

        assert len(result) == 2
        assert expected_data == list(map(lambda x: x._asdict(), result))

    def test_filter_by_selected_year(self, film_factory):
        film_factory.create_batch(
            5,
            release_data=date(year=2000, month=1, day=1),
        )
        film_factory.create_batch(
            3,
            release_data=date(year=2020, month=1, day=1),
        )
        result = Film.films.filter_by_selected_year(2000)

        assert len(result) == 5

    def test_filter_by_selected_genre(self, film_factory, genre_factory):
        genre_1 = genre_factory(name="Thriller")
        genre_2 = genre_factory(name="Comedy")
        genre_3 = genre_factory(name="Adventure")
        film_factory.create_batch(3, genre=(genre_1,))
        film_factory.create_batch(5, genre=(genre_2,))
        film_factory.create_batch(8, genre=(genre_3,))
        result = Film.films.filter_by_selected_genre("Comedy")

        assert len(result) == 5

    def test_filter_by_selected_country(self, film_factory, country_factory):
        country_1 = country_factory(name="France")
        country_2 = country_factory(name="USA")
        country_3 = country_factory(name="UK")
        film_factory.create_batch(3, country=(country_1,))
        film_factory.create_batch(5, country=(country_2,))
        film_factory.create_batch(8, country=(country_3,))
        result = Film.films.filter_by_selected_country("USA")

        assert len(result) == 5

    def test_filter_by_selected_language(self, film_factory, language_factory):
        language_1 = language_factory(name="English")
        language_2 = language_factory(name="Spain")
        language_3 = language_factory(name="French")
        film_factory.create_batch(3, language=(language_1,))
        film_factory.create_batch(5, language=(language_2,))
        film_factory.create_batch(8, language=(language_3,))
        result = Film.films.filter_by_selected_language("Spain")

        assert len(result) == 5

    def test_filter_by_selected_distributor(
        self,
        film_factory,
        distributor_factory,
    ):
        distributor_1 = distributor_factory(name="Columbia Pictures")
        distributor_2 = distributor_factory(name="Paramount Pictures")
        distributor_3 = distributor_factory(name="Universal Pictures")
        film_factory.create_batch(3, distributor=(distributor_1,))
        film_factory.create_batch(5, distributor=(distributor_2,))
        film_factory.create_batch(8, distributor=(distributor_3,))
        result = Film.films.filter_by_selected_distributor("Paramount Pictures")

        assert len(result) == 5

    def test_filter_by_selected_mpaa_rating(
        self,
        film_factory,
        mpaa_rating_factory,
    ):
        mpaa_rating_1 = mpaa_rating_factory(
            value="Not Rated",
            description="The upcoming movie",
        )
        mpaa_rating_2 = mpaa_rating_factory(
            value="R",
            description="Children under 17",
        )
        mpaa_rating_3 = mpaa_rating_factory(
            value="PG-13",
            description="Children under 13",
        )
        film_factory.create_batch(3, mpaa_rating=mpaa_rating_1)
        film_factory.create_batch(5, mpaa_rating=mpaa_rating_2)
        film_factory.create_batch(8, mpaa_rating=mpaa_rating_3)
        result = Film.films.filter_by_selected_mpaa_rating(mpaa_rating_2.pk)

        assert len(result) == 5

    def test_filter_by_search_word(self, film_factory):
        search_word = "Dark"
        film_factory(title="The Dark Knight")
        film_factory(title="Schindler's List")
        film_factory(title="The Dark Knight Rises")
        result = Film.films.filter_by_search_word(search_word)

        assert len(result) == 2

        for item in result:
            assert search_word in item.title

    def test_get_related_data(
        self,
        film_factory,
        country_factory,
        genre_factory,
        language_factory,
        news_factory,
    ):
        country_1 = country_factory()
        country_2 = country_factory()
        genre_1 = genre_factory()
        genre_2 = genre_factory()
        language_1 = language_factory()
        language_2 = language_factory()
        film_1 = film_factory(
            country=(country_1,),
            genre=(genre_1,),
            language=(language_1,),
        )
        film_2 = film_factory(
            country=(country_2,),
            genre=(genre_2,),
            language=(language_2,),
        )
        news_1 = news_factory(film=(film_1,))
        news_2 = news_factory(film=(film_2,))
        expected_data = [
            {
                "pk": film_1.pk,
                "country__name": country_1.name,
                "genre__name": genre_1.name,
                "language__name": language_1.name,
                "news__title": news_1.title,
            },
            {
                "pk": film_2.pk,
                "country__name": country_2.name,
                "genre__name": genre_2.name,
                "language__name": language_2.name,
                "news__title": news_2.title,
            },
        ]
        result = Film.films.get_related_data(
            ("country__name", "genre__name", "language__name"),
        ).order_by("pk")

        assert len(result) == 2
        assert expected_data == list(map(lambda x: x._asdict(), result))


@pytest.mark.django_db
class TestCinemaFilmPersonProfessionManager:
    def test_get_full_cast(
        self,
        cinema_person_factory,
        cinema_profession_factory,
        film_factory,
        cinema_film_person_profession_factory,
    ):
        person_1 = cinema_person_factory()
        person_2 = cinema_person_factory()
        profession_1 = cinema_profession_factory(name="Director")
        profession_2 = cinema_profession_factory(name="Actor")
        film_1 = film_factory()
        film_2 = film_factory()
        cinema_film_person_profession_factory(
            cinema_person=person_1,
            film=film_1,
            profession=profession_1,
        )
        cinema_film_person_profession_factory(
            cinema_person=person_2,
            film=film_2,
            profession=profession_2,
        )
        expected_data = [
            {
                "film__pk": film_1.pk,
                "profession__name": profession_1.name,
                "cinema_person__pk": person_1.pk,
                "cinema_person__user__first_name": person_1.user.first_name,
                "cinema_person__user__last_name": person_1.user.last_name,
            },
            {
                "film__pk": film_2.pk,
                "profession__name": profession_2.name,
                "cinema_person__pk": person_2.pk,
                "cinema_person__user__first_name": person_2.user.first_name,
                "cinema_person__user__last_name": person_2.user.last_name,
            },
        ]
        result = CinemaFilmPersonProfession.cfppm.get_full_cast()

        assert len(result) == 2
        assert expected_data == list(map(lambda x: x._asdict(), result))


@pytest.mark.django_db
class TestNewsManager:
    def test_get_brief_data(self, news_factory):
        news_1 = news_factory()
        news_2 = news_factory()
        expected_data = [
            {"pk": news_1.pk, "title": news_1.title},
            {"pk": news_2.pk, "title": news_2.title},
        ]
        result = News.news.get_brief_data().order_by("pk")
        assert len(result) == 2
        assert expected_data == list(map(lambda x: x._asdict(), result))

    def test_get_news_about_celebrities(self, news_factory):
        news_1 = news_factory()
        news_2 = news_factory()
        news_3 = news_factory()
        expected_data = [news_1, news_2, news_3]
        result = News.news.get_news_about_celebrities(
            (news_1.pk, news_2.pk, news_3.pk),
        ).order_by("pk")
        assert len(result) == 3
        assert expected_data == list(result)

    def test_filter_by_search_word(self, news_factory):
        search_word = "Quentin Tarantino"
        news_factory(
            title="Quentin Tarantino celebrates his 57th birthday",
        )
        news_factory(
            title="Brad Pitt Wins Best Supporting Actor Oscar",
        )
        news_factory(
            title="Quentin Tarantino Talks About Luke Cage Movie He Almost Made",
        )
        result = News.news.filter_by_search_word(search_word)

        assert len(result) == 2

        for item in result:
            assert search_word in item.title


@pytest.mark.django_db
class TestProductManager:
    def test_order_by_name(self, product_factory):
        product_1 = product_factory(film__title="Inglourious Basterds")
        product_2 = product_factory(film__title="Apocalypse Now")
        product_3 = product_factory(film__title="Schindler's List")
        product_4 = product_factory(film__title="Catch Me If You Can")
        expected_data = [product_2, product_4, product_1, product_3]
        result = Product.products.order_by_name()

        assert len(result) == 4
        assert expected_data == list(result)

    def test_order_by_imdb_rating(self, product_factory):
        product_1 = product_factory(film__imdb_rating__value=7.0)
        product_2 = product_factory(film__imdb_rating__value=9.0)
        product_3 = product_factory(film__imdb_rating__value=8.0)
        product_4 = product_factory(film__imdb_rating__value=8.5)
        expected_data = [product_2, product_4, product_3, product_1]
        result = Product.products.order_by_imdb_rating()

        assert len(result) == 4
        assert expected_data == list(result)

    def test_order_by_release_data(self, product_factory):
        product_1 = product_factory(
            film__release_data=date(year=2000, month=1, day=1),
        )
        product_2 = product_factory(
            film__release_data=date(year=1980, month=1, day=1),
        )
        product_3 = product_factory(
            film__release_data=date(year=2020, month=1, day=1),
        )
        product_4 = product_factory(
            film__release_data=date(year=1990, month=1, day=1),
        )
        expected_data = [product_3, product_1, product_4, product_2]
        result = Product.products.order_by_release_data()

        assert len(result) == 4
        assert expected_data == list(result)

    def test_filter_by_search_word(self, product_factory):
        search_word = "Dark"
        product_factory(film__title="The Dark Knight")
        product_factory(film__title="Schindler's List")
        product_factory(film__title="The Dark Knight Rises")
        result = Product.products.filter_by_search_word(search_word)

        assert len(result) == 2

        for item in result:
            assert search_word in item.film.title
