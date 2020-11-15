from re import (
    search,
    sub,
)

from django import template
from django.urls import reverse

from ..models import (
    CinemaPerson,
    Film,
)

register = template.Library()


@register.filter(name="get_text_hyperlinks")
def get_text_hyperlinks(text):
    """Custom filter for getting hyperlinks in text."""
    brief_persons_data = CinemaPerson.persons.get_brief_data()
    for person in brief_persons_data:
        person_name = f"{person.user__first_name} {person.user__last_name}"
        match = search(fr"\s?(?i:{person_name})\s?", text)
        if match:
            url_path = reverse(
                "cinema:movie-person-detail", kwargs={"pk": person.pk}
            )
            found_person = match.group()
            text = sub(
                found_person.strip(),
                f"<a href='{url_path}'>{person_name}</a>",
                text,
            )
    brief_films_data = Film.films.get_brief_data()
    for film in brief_films_data:
        match = search(fr"\s?{film.title}\s?", text)
        if match:
            url_path = reverse("cinema:film-detail", args=(film.pk,))
            found_film = match.group()
            text = sub(
                found_film.strip(),
                f"<a href='{url_path}'>{film.title}</a>",
                text,
            )
    return text
