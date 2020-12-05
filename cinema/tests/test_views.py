import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from cinema.models import Film


@pytest.mark.django_db
class TestProductListView:
    def test_view_url_exists_at_desired_location(
        self, client, create_12_products
    ):
        response = client.get("/blu-ray-films/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_12_products):
        response = client.get(reverse("cinema:product-list"))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_12_products):
        response = client.get(reverse("cinema:product-list"))
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/product_list.html")

    def test_pagination_is_eight(self, client, create_12_products):
        response = client.get(reverse("cinema:product-list"))
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert response.context["is_paginated"]
        assert len(response.context["product_list"]) == 8

    def test_view_returns_all_products(self, client, create_12_products):
        response = client.get(reverse("cinema:product-list") + "?page=2")
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert response.context["is_paginated"]
        assert len(response.context["product_list"]) == 4

    def test_view_uses_default_ordering(self, client, create_12_products):
        response = client.get(reverse("cinema:product-list"))
        assert response.status_code == 200
        assert not response.context["view"].ordering


@pytest.mark.django_db
class TestTopRatedProductListView:
    def test_view_url_exists_at_desired_location(
        self, client, create_12_products
    ):
        response = client.get("/blu-ray-films/by-top-rated/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_12_products):
        response = client.get(reverse("cinema:top-rated-product-list"))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_12_products):
        response = client.get(reverse("cinema:top-rated-product-list"))
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/product_list.html")

    def test_pagination_is_eight(self, client, create_12_products):
        response = client.get(reverse("cinema:top-rated-product-list"))
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert response.context["is_paginated"]
        assert len(response.context["product_list"]) == 8

    def test_view_returns_all_products(self, client, create_12_products):
        response = client.get(
            reverse("cinema:top-rated-product-list") + "?page=2"
        )
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert response.context["is_paginated"]
        assert len(response.context["product_list"]) == 4

    def test_view_uses_correct_ordering(self, client, create_12_products):
        response = client.get(reverse("cinema:top-rated-product-list"))
        assert response.status_code == 200
        assert response.context["view"].ordering == "-film__imdb_rating__value"


@pytest.mark.django_db
class TestNewReleasesProductListView:
    def test_view_url_exists_at_desired_location(
        self, client, create_12_products
    ):
        response = client.get("/blu-ray-films/new-releases/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_12_products):
        response = client.get(reverse("cinema:new-releases-product-list"))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_12_products):
        response = client.get(reverse("cinema:new-releases-product-list"))
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/product_list.html")

    def test_pagination_is_eight(self, client, create_12_products):
        response = client.get(reverse("cinema:new-releases-product-list"))
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert response.context["is_paginated"]
        assert len(response.context["product_list"]) == 8

    def test_view_returns_all_products(self, client, create_12_products):
        response = client.get(
            reverse("cinema:new-releases-product-list") + "?page=2"
        )
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert response.context["is_paginated"]
        assert len(response.context["product_list"]) == 4

    def test_view_uses_correct_ordering(self, client, create_12_products):
        response = client.get(reverse("cinema:new-releases-product-list"))
        assert response.status_code == 200
        assert response.context["view"].ordering == "-film__release_data"


@pytest.mark.django_db
class TestFilmListView:
    def test_view_url_exists_at_desired_location(self, client, create_12_films):
        response = client.get("/films/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_12_films):
        response = client.get(reverse("cinema:film-list"))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_12_films):
        response = client.get(reverse("cinema:film-list"))
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/film_list.html")

    def test_pagination_is_eight(self, client, create_12_films):
        response = client.get(reverse("cinema:film-list"))
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert response.context["is_paginated"]
        assert len(response.context["film_list"]) == 8

    def test_view_returns_all_films(self, client, create_12_films):
        response = client.get(reverse("cinema:film-list") + "?page=2")
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert response.context["is_paginated"]
        assert len(response.context["film_list"]) == 4

    def test_view_uses_default_ordering(self, client, create_12_films):
        response = client.get(reverse("cinema:film-list"))
        assert response.status_code == 200
        assert not response.context["view"].ordering


@pytest.mark.django_db
class TestTopRatedFilmListView:
    def test_view_url_exists_at_desired_location(self, client, create_12_films):
        response = client.get("/films/by-top-rated/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_12_films):
        response = client.get(reverse("cinema:top-rated-film-list"))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_12_films):
        response = client.get(reverse("cinema:top-rated-film-list"))
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/film_list.html")

    def test_pagination_is_eight(self, client, create_12_films):
        response = client.get(reverse("cinema:top-rated-film-list"))
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert response.context["is_paginated"]
        assert len(response.context["film_list"]) == 8

    def test_view_returns_all_films(self, client, create_12_films):
        response = client.get(reverse("cinema:top-rated-film-list") + "?page=2")
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert response.context["is_paginated"]
        assert len(response.context["film_list"]) == 4

    def test_view_uses_correct_ordering(self, client, create_12_films):
        response = client.get(reverse("cinema:top-rated-film-list"))
        assert response.status_code == 200
        assert response.context["view"].ordering == "-imdb_rating__value"


@pytest.mark.django_db
class TestBudgetFilmListView:
    def test_view_url_exists_at_desired_location(self, client, create_12_films):
        response = client.get("/films/by-budget/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_12_films):
        response = client.get(reverse("cinema:budget-film-list"))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_12_films):
        response = client.get(reverse("cinema:budget-film-list"))
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/film_list.html")

    def test_pagination_is_eight(self, client, create_12_films):
        response = client.get(reverse("cinema:budget-film-list"))
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert response.context["is_paginated"]
        assert len(response.context["film_list"]) == 8

    def test_view_returns_all_films(self, client, create_12_films):
        response = client.get(reverse("cinema:budget-film-list") + "?page=2")
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert response.context["is_paginated"]
        assert len(response.context["film_list"]) == 4

    def test_view_uses_correct_ordering(self, client, create_12_films):
        response = client.get(reverse("cinema:budget-film-list"))
        assert response.status_code == 200
        assert response.context["view"].ordering == "-budget"


@pytest.mark.django_db
class TestUsaGrossFilmListView:
    def test_view_url_exists_at_desired_location(self, client, create_12_films):
        response = client.get("/films/by-usa-gross/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_12_films):
        response = client.get(reverse("cinema:usa-gross-film-list"))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_12_films):
        response = client.get(reverse("cinema:usa-gross-film-list"))
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/film_list.html")

    def test_pagination_is_eight(self, client, create_12_films):
        response = client.get(reverse("cinema:usa-gross-film-list"))
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert response.context["is_paginated"]
        assert len(response.context["film_list"]) == 8

    def test_view_returns_all_films(self, client, create_12_films):
        response = client.get(reverse("cinema:usa-gross-film-list") + "?page=2")
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert response.context["is_paginated"]
        assert len(response.context["film_list"]) == 4

    def test_view_uses_correct_ordering(self, client, create_12_films):
        response = client.get(reverse("cinema:usa-gross-film-list"))
        assert response.status_code == 200
        assert response.context["view"].ordering == "-usa_gross"


@pytest.mark.django_db
class TestWorldGrossFilmListView:
    def test_view_url_exists_at_desired_location(self, client, create_12_films):
        response = client.get("/films/by-world-gross/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_12_films):
        response = client.get(reverse("cinema:world-gross-film-list"))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_12_films):
        response = client.get(reverse("cinema:world-gross-film-list"))
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/film_list.html")

    def test_pagination_is_eight(self, client, create_12_films):
        response = client.get(reverse("cinema:world-gross-film-list"))
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert response.context["is_paginated"]
        assert len(response.context["film_list"]) == 8

    def test_view_returns_all_films(self, client, create_12_films):
        response = client.get(
            reverse("cinema:world-gross-film-list") + "?page=2"
        )
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert response.context["is_paginated"]
        assert len(response.context["film_list"]) == 4

    def test_view_uses_correct_ordering(self, client, create_12_films):
        response = client.get(reverse("cinema:world-gross-film-list"))
        assert response.status_code == 200
        assert response.context["view"].ordering == "-world_gross"


@pytest.mark.django_db
class TestYearFilmListView:
    def test_view_url_exists_at_desired_location(self, client, create_12_films):
        selected_year = Film.objects.first().year
        response = client.get(f"/films/by-year/{selected_year}/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_12_films):
        selected_year = Film.objects.first().year
        response = client.get(
            reverse("cinema:year-film-list", args=(selected_year,))
        )
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_12_films):
        selected_year = Film.objects.first().year
        response = client.get(
            reverse("cinema:year-film-list", args=(selected_year,))
        )
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/film_list.html")

    def test_view_returns_films_of_selected_year(self, client, create_12_films):
        selected_year = Film.objects.first().year
        response = client.get(
            reverse("cinema:year-film-list", args=(selected_year,))
        )
        assert response.status_code == 200

        for film in response.context["film_list"]:
            assert film.year == selected_year


@pytest.mark.django_db
class TestGenreFilmListView:
    def test_view_url_exists_at_desired_location(self, client, create_12_films):
        selected_genre = Film.objects.first().genre.first().name
        response = client.get(f"/films/by-genre/{selected_genre}/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_12_films):
        selected_genre = Film.objects.first().genre.first().name
        response = client.get(
            reverse("cinema:genre-film-list", args=(selected_genre,))
        )
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_12_films):
        selected_genre = Film.objects.first().genre.first().name
        response = client.get(
            reverse("cinema:genre-film-list", args=(selected_genre,))
        )
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/film_list.html")

    def test_view_returns_films_of_selected_genre(
        self, client, create_12_films
    ):
        selected_genre = Film.objects.first().genre.first().name
        response = client.get(
            reverse("cinema:genre-film-list", args=(selected_genre,))
        )
        assert response.status_code == 200

        for film in response.context["film_list"]:
            assert film.genre.first().name == selected_genre


@pytest.mark.django_db
class TestCountryFilmListView:
    def test_view_url_exists_at_desired_location(self, client, create_12_films):
        selected_country = Film.objects.first().country.first().name
        response = client.get(f"/films/by-country/{selected_country}/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_12_films):
        selected_country = Film.objects.first().country.first().name
        response = client.get(
            reverse("cinema:country-film-list", args=(selected_country,))
        )
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_12_films):
        selected_country = Film.objects.first().country.first().name
        response = client.get(
            reverse("cinema:country-film-list", args=(selected_country,))
        )
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/film_list.html")

    def test_view_returns_films_of_selected_country(
        self, client, create_12_films
    ):
        selected_country = Film.objects.first().country.first().name
        response = client.get(
            reverse("cinema:country-film-list", args=(selected_country,))
        )
        assert response.status_code == 200

        for film in response.context["film_list"]:
            assert film.country.first().name == selected_country


@pytest.mark.django_db
class TestLanguageFilmListView:
    def test_view_url_exists_at_desired_location(self, client, create_12_films):
        selected_language = Film.objects.first().language.first().name
        response = client.get(f"/films/by-language/{selected_language}/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_12_films):
        selected_language = Film.objects.first().language.first().name
        response = client.get(
            reverse("cinema:language-film-list", args=(selected_language,))
        )
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_12_films):
        selected_language = Film.objects.first().language.first().name
        response = client.get(
            reverse("cinema:language-film-list", args=(selected_language,))
        )
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/film_list.html")

    def test_view_returns_films_of_selected_language(
        self, client, create_12_films
    ):
        selected_language = Film.objects.first().language.first().name
        response = client.get(
            reverse("cinema:language-film-list", args=(selected_language,))
        )
        assert response.status_code == 200

        for film in response.context["film_list"]:
            assert film.language.first().name == selected_language


@pytest.mark.django_db
class TestDistributorFilmListView:
    def test_view_url_exists_at_desired_location(self, client, create_12_films):
        selected_distributor = Film.objects.first().distributor.first().name
        response = client.get(f"/films/by-distributor/{selected_distributor}/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_12_films):
        selected_distributor = Film.objects.first().distributor.first().name
        response = client.get(
            reverse(
                "cinema:distributor-film-list", args=(selected_distributor,)
            )
        )
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_12_films):
        selected_distributor = Film.objects.first().distributor.first().name
        response = client.get(
            reverse(
                "cinema:distributor-film-list", args=(selected_distributor,)
            )
        )
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/film_list.html")

    def test_view_returns_films_of_selected_distributor(
        self, client, create_12_films
    ):
        selected_distributor = Film.objects.first().distributor.first().name
        response = client.get(
            reverse(
                "cinema:distributor-film-list", args=(selected_distributor,)
            )
        )
        assert response.status_code == 200

        for film in response.context["film_list"]:
            assert film.distributor.first().name == selected_distributor


@pytest.mark.django_db
class TestMpaaFilmListView:
    def test_view_url_exists_at_desired_location(self, client, create_12_films):
        selected_mpaa = Film.objects.first().mpaa_rating.pk
        response = client.get(f"/films/by-mpaa/{selected_mpaa}/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_12_films):
        selected_mpaa = Film.objects.first().mpaa_rating.pk
        response = client.get(
            reverse("cinema:mpaa-film-list", args=(selected_mpaa,))
        )
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_12_films):
        selected_mpaa = Film.objects.first().mpaa_rating.pk
        response = client.get(
            reverse("cinema:mpaa-film-list", args=(selected_mpaa,))
        )
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/film_list.html")

    def test_view_returns_films_of_selected_mpaa(self, client, create_12_films):
        selected_mpaa = Film.objects.first().mpaa_rating.pk
        response = client.get(
            reverse("cinema:mpaa-film-list", args=(selected_mpaa,))
        )
        assert response.status_code == 200

        for film in response.context["film_list"]:
            assert film.mpaa_rating.pk == selected_mpaa


@pytest.mark.django_db
class TestNewsListView:
    def test_view_url_exists_at_desired_location(self, client, create_12_news):
        response = client.get("/news/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_12_news):
        response = client.get(reverse("cinema:news-list"))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_12_news):
        response = client.get(reverse("cinema:news-list"))
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/news_list.html")

    def test_pagination_is_five(self, client, create_12_news):
        response = client.get(reverse("cinema:news-list"))
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert response.context["is_paginated"]
        assert len(response.context["news_list"]) == 5

    def test_view_returns_all_news(self, client, create_12_news):
        response = client.get(reverse("cinema:news-list") + "?page=3")
        assert response.status_code == 200
        assert "is_paginated" in response.context
        assert response.context["is_paginated"]
        assert len(response.context["news_list"]) == 2

    def test_view_uses_default_ordering(self, client, create_12_news):
        response = client.get(reverse("cinema:news-list"))
        assert response.status_code == 200
        assert not response.context["view"].ordering


@pytest.mark.django_db
class TestCelebrityNewsListView:
    def test_view_url_exists_at_desired_location(self, client, create_12_news):
        response = client.get("/news/celebrities/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, create_12_news):
        response = client.get(reverse("cinema:celebrity-news-list"))
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, create_12_news):
        response = client.get(reverse("cinema:celebrity-news-list"))
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/news_list.html")


@pytest.mark.django_db
class TestFilmDetail:
    def test_view_url_exists_at_desired_location(self, client, test_film):
        response = client.get(f"/films/{test_film.pk}/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, test_film):
        response = client.get(
            reverse("cinema:film-detail", args=(test_film.pk,))
        )
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, test_film):
        response = client.get(
            reverse("cinema:film-detail", args=(test_film.pk,))
        )
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/film_detail.html")

    def test_view_returns_http404_for_invalid_film(self, client, test_film):
        invalid_pk = 10
        response = client.get(reverse("cinema:film-detail", args=(invalid_pk,)))
        assert response.status_code == 404

    def test_view_returns_form_to_add_film_comment_if_user_is_logged_in(
        self, client, create_logged_in_user, test_film
    ):
        response = client.get(
            reverse("cinema:film-detail", args=(test_film.pk,))
        )
        assert response.status_code == 200
        assert response.context["form"].initial["film"] == test_film.pk
        assert response.context["form"].initial["author"] == "test.username"
        assert "captcha" not in response.context["form"].fields

    def test_view_returns_form_to_add_film_comment_if_user_is_logged_out(
        self, client, test_film
    ):
        response = client.get(
            reverse("cinema:film-detail", args=(test_film.pk,))
        )
        assert response.status_code == 200
        assert response.context["form"].initial["film"] == test_film.pk
        assert "author" not in response.context["form"].initial
        assert response.context["form"].fields["captcha"]

    def test_view_returns_all_film_comments(
        self, client, test_film, comment_to_film_factory
    ):
        comment_to_film_factory.create_batch(size=10, film=test_film)
        response = client.get(
            reverse("cinema:film-detail", args=(test_film.pk,))
        )
        assert response.status_code == 200
        assert response.context["film"].commenttofilm_set.count() == 10

    def test_view_returns_new_film_comment_after_getting_of_valid_form_data(
        self, client, create_logged_in_user, test_film
    ):
        form_data = {
            "author": "test.username",
            "content": "Very nice film",
            "film": test_film.pk,
        }
        response = client.post(
            path=reverse("cinema:film-detail", args=(test_film.pk,)),
            data=form_data,
        )
        assert response.status_code == 200
        assert response.context["film"].commenttofilm_set.count() == 1

        new_comment = response.context["film"].commenttofilm_set.first()

        assert new_comment.author == "test.username"
        assert new_comment.content == "Very nice film"
        assert new_comment.film.pk == test_film.pk

        for message in response.context["messages"]:
            if message.tags == "success":
                assert message.message == "Comment added"

    def test_view_returns_form_with_errors_after_getting_of_invalid_form_data(
        self, client, test_film
    ):
        response = client.post(
            path=reverse("cinema:film-detail", args=(test_film.pk,)),
            data={},
        )
        assert not response.context["form"].is_valid()

        for message in response.context["messages"]:
            if message.tags == "warning":
                assert message.message == "No Comment added"


@pytest.mark.django_db
class TestProductDetail:
    def test_view_url_exists_at_desired_location(self, client, test_product):
        response = client.get(f"/blu-ray-films/{test_product.pk}/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, test_product):
        response = client.get(
            reverse("cinema:product-detail", args=(test_product.pk,))
        )
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, test_product):
        response = client.get(
            reverse("cinema:product-detail", args=(test_product.pk,))
        )
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/product_detail.html")

    def test_view_returns_http404_for_invalid_product(
        self, client, test_product
    ):
        invalid_pk = 10
        response = client.get(
            reverse("cinema:product-detail", args=(invalid_pk,))
        )
        assert response.status_code == 404

    def test_view_returns_form_to_add_product_comment_if_user_is_logged_in(
        self, client, create_logged_in_user, test_product
    ):
        response = client.get(
            reverse("cinema:product-detail", args=(test_product.pk,))
        )
        assert response.status_code == 200
        assert response.context["form"].initial["product"] == test_product.pk
        assert response.context["form"].initial["author"] == "test.username"
        assert "captcha" not in response.context["form"].fields

    def test_view_returns_form_to_add_product_comment_if_user_is_logged_out(
        self, client, test_product
    ):
        response = client.get(
            reverse("cinema:product-detail", args=(test_product.pk,))
        )
        assert response.status_code == 200
        assert response.context["form"].initial["product"] == test_product.pk
        assert "author" not in response.context["form"].initial
        assert response.context["form"].fields["captcha"]

    def test_view_returns_all_product_comments(
        self, client, test_product, comment_to_product_factory
    ):
        comment_to_product_factory.create_batch(size=10, product=test_product)
        response = client.get(
            reverse("cinema:product-detail", args=(test_product.pk,))
        )
        assert response.status_code == 200
        assert response.context["product"].commenttoproduct_set.count() == 10

    def test_view_returns_new_product_comment_after_getting_of_valid_form_data(
        self, client, create_logged_in_user, test_product
    ):
        form_data = {
            "author": "test.username",
            "content": "Very nice product",
            "product": test_product.pk,
        }
        response = client.post(
            path=reverse("cinema:product-detail", args=(test_product.pk,)),
            data=form_data,
        )
        assert response.status_code == 200
        assert response.context["product"].commenttoproduct_set.count() == 1

        new_comment = response.context["product"].commenttoproduct_set.first()

        assert new_comment.author == "test.username"
        assert new_comment.content == "Very nice product"
        assert new_comment.product.pk == test_product.pk

        for message in response.context["messages"]:
            if message.tags == "success":
                assert message.message == "Comment added"

    def test_view_returns_form_with_errors_after_getting_of_invalid_form_data(
        self, client, test_product
    ):
        response = client.post(
            path=reverse("cinema:product-detail", args=(test_product.pk,)),
            data={},
        )
        assert not response.context["form"].is_valid()

        for message in response.context["messages"]:
            if message.tags == "warning":
                assert message.message == "No Comment added"


@pytest.mark.django_db
class TestCinemaPersonDetail:
    def test_view_url_exists_at_desired_location(self, client, test_person):
        response = client.get(f"/movie-persons/{test_person.pk}/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, test_person):
        response = client.get(
            reverse("cinema:movie-person-detail", args=(test_person.pk,))
        )
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, test_person):
        response = client.get(
            reverse("cinema:movie-person-detail", args=(test_person.pk,))
        )
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/cinema_person_detail.html")

    def test_view_returns_http404_for_invalid_person(self, client, test_person):
        invalid_pk = 10
        response = client.get(
            reverse("cinema:movie-person-detail", args=(invalid_pk,))
        )
        assert response.status_code == 404

    def test_view_returns_form_to_add_person_comment_if_user_is_logged_in(
        self, client, create_logged_in_user, test_person
    ):
        response = client.get(
            reverse("cinema:movie-person-detail", args=(test_person.pk,))
        )
        assert response.status_code == 200
        assert (
            response.context["form"].initial["cinema_person"] == test_person.pk
        )
        assert response.context["form"].initial["author"] == "test.username"
        assert "captcha" not in response.context["form"].fields

    def test_view_returns_form_to_add_person_comment_if_user_is_logged_out(
        self, client, test_person
    ):
        response = client.get(
            reverse("cinema:movie-person-detail", args=(test_person.pk,))
        )
        assert response.status_code == 200
        assert (
            response.context["form"].initial["cinema_person"] == test_person.pk
        )
        assert "author" not in response.context["form"].initial
        assert response.context["form"].fields["captcha"]

    def test_view_returns_all_person_comments(
        self, client, test_person, comment_to_person_factory
    ):
        comment_to_person_factory.create_batch(
            size=10, cinema_person=test_person
        )
        response = client.get(
            reverse("cinema:movie-person-detail", args=(test_person.pk,))
        )
        assert response.status_code == 200
        assert (
            response.context["cinema_person"].commenttoperson_set.count() == 10
        )

    def test_view_returns_new_person_comment_after_getting_of_valid_form_data(
        self, client, create_logged_in_user, test_person
    ):
        form_data = {
            "author": "test.username",
            "content": "Very nice cinema person",
            "cinema_person": test_person.pk,
        }
        response = client.post(
            path=reverse("cinema:movie-person-detail", args=(test_person.pk,)),
            data=form_data,
        )
        assert response.status_code == 200
        assert (
            response.context["cinema_person"].commenttoperson_set.count() == 1
        )

        new_comment = response.context[
            "cinema_person"
        ].commenttoperson_set.first()

        assert new_comment.author == "test.username"
        assert new_comment.content == "Very nice cinema person"
        assert new_comment.cinema_person.pk == test_person.pk

        for message in response.context["messages"]:
            if message.tags == "success":
                assert message.message == "Comment added"

    def test_view_returns_form_with_errors_after_getting_of_invalid_form_data(
        self, client, test_person
    ):
        response = client.post(
            path=reverse("cinema:movie-person-detail", args=(test_person.pk,)),
            data={},
        )
        assert not response.context["form"].is_valid()

        for message in response.context["messages"]:
            if message.tags == "warning":
                assert message.message == "No Comment added"


@pytest.mark.django_db
class TestNewsDetail:
    def test_view_url_exists_at_desired_location(self, client, test_news):
        response = client.get(f"/news/{test_news.pk}/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(self, client, test_news):
        response = client.get(
            reverse("cinema:news-detail", args=(test_news.pk,))
        )
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, test_news):
        response = client.get(
            reverse("cinema:news-detail", args=(test_news.pk,))
        )
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/news_detail.html")

    def test_view_returns_http404_for_invalid_news(self, client, test_news):
        invalid_pk = 10
        response = client.get(reverse("cinema:news-detail", args=(invalid_pk,)))
        assert response.status_code == 404

    def test_view_returns_form_to_add_news_comment_if_user_is_logged_in(
        self, client, create_logged_in_user, test_news
    ):
        response = client.get(
            reverse("cinema:news-detail", args=(test_news.pk,))
        )
        assert response.status_code == 200
        assert response.context["form"].initial["news"] == test_news.pk
        assert response.context["form"].initial["author"] == "test.username"
        assert "captcha" not in response.context["form"].fields

    def test_view_returns_form_to_add_news_comment_if_user_is_logged_out(
        self, client, test_news
    ):
        response = client.get(
            reverse("cinema:news-detail", args=(test_news.pk,))
        )
        assert response.status_code == 200
        assert response.context["form"].initial["news"] == test_news.pk
        assert "author" not in response.context["form"].initial
        assert response.context["form"].fields["captcha"]

    def test_view_returns_all_news_comments(
        self, client, test_news, comment_to_news_factory
    ):
        comment_to_news_factory.create_batch(size=10, news=test_news)
        response = client.get(
            reverse("cinema:news-detail", args=(test_news.pk,))
        )
        assert response.status_code == 200
        assert response.context["news"].commenttonews_set.count() == 10

    def test_view_returns_new_news_comment_after_getting_of_valid_form_data(
        self, client, create_logged_in_user, test_news
    ):
        form_data = {
            "author": "test.username",
            "content": "Very nice news",
            "news": test_news.pk,
        }
        response = client.post(
            path=reverse("cinema:news-detail", args=(test_news.pk,)),
            data=form_data,
        )
        assert response.status_code == 200
        assert response.context["news"].commenttonews_set.count() == 1

        new_comment = response.context["news"].commenttonews_set.first()

        assert new_comment.author == "test.username"
        assert new_comment.content == "Very nice news"
        assert new_comment.news.pk == test_news.pk

        for message in response.context["messages"]:
            if message.tags == "success":
                assert message.message == "Comment added"

    def test_view_returns_form_with_errors_after_getting_of_invalid_form_data(
        self, client, test_news
    ):
        response = client.post(
            path=reverse("cinema:news-detail", args=(test_news.pk,)),
            data={},
        )
        assert not response.context["form"].is_valid()

        for message in response.context["messages"]:
            if message.tags == "warning":
                assert message.message == "No Comment added"


@pytest.mark.django_db
class TestIndexView:
    def test_view_url_exists_at_desired_location(
        self, client, create_12_films_products_news
    ):
        response = client.get("/")
        assert response.status_code == 200

    def test_view_url_accessible_by_name(
        self, client, create_12_films_products_news
    ):
        response = client.get(reverse("cinema:index"))
        assert response.status_code == 200

    def test_view_uses_correct_template(
        self, client, create_12_films_products_news
    ):
        response = client.get(reverse("cinema:index"))
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/index.html")


@pytest.mark.django_db
class TestSearchResultsView:
    def test_view_url_accessible_by_name_after_search(self, client, test_film):
        response = client.get(
            path=reverse("cinema:search-results"),
            data={"q": "Steven Spielberg"},
        )
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client, test_film):
        response = client.get(
            path=reverse("cinema:search-results"),
            data={"q": "Steven Spielberg"},
        )
        assert response.status_code == 200
        assertTemplateUsed(response, "cinema/search_results.html")

    def test_view_returns_all_results_of_search(self, client, test_film):
        response = client.get(
            path=reverse("cinema:search-results"),
            data={"q": "Steven Spielberg"},
        )
        assert response.status_code == 200
        assert len(response.context["person_list"]) == 1
        assert response.context["person_list"].get(
            user__first_name="Steven", user__last_name="Spielberg"
        )
