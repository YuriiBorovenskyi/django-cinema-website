from .models import (
    Film,
    CinemaPerson,
    News,
    CinemaFilmPersonProfession,
)


def get_films_ratings_sets():
    """
    Get sets from top 5 movies ordered by differ criterion name.
    """
    criteria = ("imdb_rating__value", "budget", "usa_gross", "world_gross")
    cached_films_data = Film.films.all()
    films_ratings_sets = {}
    for criterion in criteria:
        top_5 = cached_films_data.order_by(f"-{criterion}")[:5].values_list(
            "pk", "title", f"{criterion}", named=True
        )
        films_ratings_sets[criterion] = top_5
    return films_ratings_sets


def get_cast_and_crew():
    """
    Get cast and crew by professions for all movies.
    """
    professions = ("Director", "Actor", "Writer")
    films_full_cast = CinemaFilmPersonProfession.cfppm.get_full_cast()
    cast_and_crew = {}
    for cast in films_full_cast:
        if cast.film__pk not in cast_and_crew:
            cast_and_crew[cast.film__pk] = {}
            for profession in professions:
                cast_and_crew[cast.film__pk][profession] = []
        cast_and_crew[cast.film__pk][cast.profession__name].append(
            {"pk": cast.cinema_person__pk,
             "name": f"{cast.cinema_person__user__first_name} "
                     f"{cast.cinema_person__user__last_name}"}
        )
    return cast_and_crew


def get_films_info():
    """
    Get information about all movies from related models.
    """
    film_fields = (
        "country__name", "genre__name", "language__name",
        "distributor__name", "news__pk"
    )
    films_data = Film.films.get_related_data(film_fields)

    films_info = {}
    for film in films_data:
        if film.pk not in films_info:
            films_info[film.pk] = {}

        for field in film_fields:
            if "news" not in films_info[film.pk]:
                films_info[film.pk]["news"] = {}
            if field == "news__pk" and film.news__pk and film.news__pk \
                    not in films_info[film.pk]["news"]:
                films_info[film.pk]["news"][film.news__pk] = film.news__title
            else:
                if field not in films_info[film.pk]:
                    films_info[film.pk][field] = []
                if field == "country__name" and film.country__name not in \
                        films_info[film.pk][field]:
                    films_info[film.pk][field].append(film.country__name)
                elif field == "genre__name" and film.genre__name not in \
                        films_info[film.pk][field]:
                    films_info[film.pk][field].append(film.genre__name)
                elif field == "language__name" and film.language__name \
                        not in films_info[film.pk][field]:
                    films_info[film.pk][field].append(film.language__name)
                elif field == "distributor__name" and film.distributor__name \
                        not in films_info[film.pk][field]:
                    films_info[film.pk][field].append(film.distributor__name)
    return films_info


def get_persons_info():
    """
    Get information about all cinema persons from related models.
    """
    person_fields = ("film__genre__name", "news__pk")
    persons_data = CinemaPerson.persons.get_related_data(
        person_fields
    )
    persons_info = {}
    for person in persons_data:
        if person.pk not in persons_info:
            persons_info[person.pk] = {}
        for field in person_fields:
            if "news" not in persons_info[person.pk]:
                persons_info[person.pk]["news"] = {}
            if field == "film__genre__name":
                if field not in persons_info[person.pk]:
                    persons_info[person.pk][field] = []
                if person.film__genre__name not in \
                        persons_info[person.pk][field]:
                    persons_info[person.pk][field].append(
                        person.film__genre__name
                    )
            elif field == "news__pk" and person.news__pk and person.news__pk \
                    not in persons_info[person.pk]["news"]:
                persons_info[person.pk]["news"][person.news__pk] = \
                    person.news__title
    return persons_info


def get_celebrity_news_id():
    """
    Get id of news related to celebrities.
    """
    persons_data = CinemaPerson.persons.get_brief_data()
    celebrities = [
        f"{person.user__first_name} {person.user__last_name}" for person in
        persons_data
    ]
    news_data = News.news.get_brief_data()
    news_titles = {news.pk: news.title for news in news_data}
    celebrity_news_id = []
    for pk, title in news_titles.items():
        for celebrity in celebrities:
            if celebrity in title:
                celebrity_news_id.append(pk)
                break
    return celebrity_news_id


def get_filmography_and_extra_info(cinema_person):
    """
    Get filmography and extra information about all cinema persons.
    """
    person_professions = sorted(
        set(
            cinema_person.cinemafilmpersonprofession_set.values_list(
                "profession__name", flat=True
            )
        )
    )
    filmography = {}
    for person_profession in person_professions:
        films_for_profession = cinema_person.film_set.filter(
            cinemafilmpersonprofession__profession__name=person_profession
        ).values_list(
            "pk", "title", "release_data__year", "imdb_rating__value",
            named=True
        ).order_by("-release_data")
        filmography[person_profession] = films_for_profession

    films_number = []
    films_years = []
    for person_films in filmography.values():
        for person_film in person_films:
            films_number.append(person_film.pk)
            films_years.append(person_film.release_data__year)

    return (
        filmography, tuple(person_professions), len(films_number),
        f'{min(films_years)} - {max(films_years)}'
    )
