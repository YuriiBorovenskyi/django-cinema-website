from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, TemplateView

from .forms import UserCommentToProductForm, GuestCommentToProductForm, \
    UserCommentToFilmForm, GuestCommentToFilmForm, UserCommentToPersonForm, \
    GuestCommentToPersonForm, UserCommentToNewsForm, GuestCommentToNewsForm
from .models import Product, News, Film, CinemaPerson, MpaaRating, \
    CommentToProduct, CommentToFilm, CommentToPerson, CommentToNews

all_films = Film.objects.prefetch_related(
    "staff__cinemafilmpersonprofession_set__profession", "staff__user",
    "country", "genre", "language", "distributor", "news_set"
).select_related("imdb_rating", "mpaa_rating", "product")

top_films = all_films.values_list(
    "pk", "title", "imdb_rating__value", "budget", "usa_gross",
    "world_gross", named=True
)
imdb_top_5 = top_films.order_by("-imdb_rating__value")[:5]
budget_top_5 = top_films.order_by("-budget")[:5]
usa_gross_top_5 = top_films.order_by("-usa_gross")[:5]
world_gross_top_5 = top_films.order_by("-world_gross")[:5]

professions = ("Director", "Actor", "Writer")
persons_by_films = {}

for film in all_films:
    persons_by_films[film.pk] = {}

    for profession in professions:
        persons_by_films[film.pk][profession] = []
        film_persons = film.staff.filter(
            cinemafilmpersonprofession__profession__name=profession
        ).order_by("pk").values_list(
            "pk", "user__first_name", "user__last_name", named=True
        )
        for person in film_persons:
            persons_by_films[film.pk][profession].append(
                {"pk": person.pk,
                 "name": f"{person.user__first_name} "
                         f"{person.user__last_name}"}
            )
film_fields = (
    "country__name", "genre__name", "language__name",
    "distributor__name", "news__pk", "news__title"
)
info_by_films_qs = all_films.values_list(
    "pk", *film_fields, named=True
).order_by("-news__created_at")

info_by_films = {}
for film in info_by_films_qs:
    if film.pk not in info_by_films:
        info_by_films[film.pk] = {}

    for field in film_fields:
        if field not in ("news__pk", "news__title"):
            if field not in info_by_films[film.pk]:
                info_by_films[film.pk][field] = []
            if field == "country__name" and film.country__name not in \
                    info_by_films[film.pk][field]:
                info_by_films[film.pk][field].append(film.country__name)
            elif field == "genre__name" and film.genre__name not in \
                    info_by_films[film.pk][field]:
                info_by_films[film.pk][field].append(film.genre__name)
            elif field == "language__name" and film.language__name not in \
                    info_by_films[film.pk][field]:
                info_by_films[film.pk][field].append(film.language__name)
            elif field == "distributor__name" and film.distributor__name \
                    not in info_by_films[film.pk][field]:
                info_by_films[film.pk][field].append(film.distributor__name)
        else:
            if "news" not in info_by_films[film.pk]:
                info_by_films[film.pk]["news"] = {}
            if field == "news__pk" and film.news__pk and film.news__pk not in \
                    info_by_films[film.pk]["news"]:
                info_by_films[film.pk]["news"][film.news__pk] = film.news__title

all_persons = CinemaPerson.objects.prefetch_related(
    "film_set__genre", "film_set__imdb_rating", "news_set"
).select_related("user")


class ProductListView(ListView):
    model = Product
    paginate_by = 8

    def get_queryset(self):
        return super().get_queryset().select_related("film").only(
            "pk", "price", "film", "in_stock"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Movies on Blu-ray',
            'persons_by_films': persons_by_films
        })
        return context


class TopRatedProductListView(ProductListView):
    ordering = "-film__imdb_rating__value"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Top Rated Movies on Blu-ray'
        return context


class NewReleasesProductListView(ProductListView):
    ordering = "-film__release_data"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'New Releases Movies on Blu-ray'
        return context


class IndexView(TemplateView):
    template_name = 'cinema/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_rated_list = Product.objects.select_related("film").only(
            "pk", "price", "film", "in_stock"
        ).order_by("-film__imdb_rating__value")
        new_releases_list = top_rated_list.order_by("-film__release_data")
        news_list = News.objects.only(
            "pk", "title", "news_source", "news_detail_photo", "created_at"
        )
        context.update({
            'page_title': "Latest Movie News, Movies on Blu-ray",
            'title_news': "Cinema News",
            'description_news': "The latest movie news on the movies 'you're "
                                "most interested in seeing.",
            'title_blu_ray': "Movies on Blu-ray",
            'description_blu_ray': "Welcome to the fantastic Blu-ray "
                                   "department here, where you can find the "
                                   "films, you could ever want to see in "
                                   "superb high definition quality. We're "
                                   "constantly adding all of the latest "
                                   "Blu-ray releases to our collection and "
                                   "always have an unbelievable offer or two. "
                                   "We promise great deals on the best films!",
            'title_top_rated': 'Top Rated',
            'title_new_releases': 'New Releases',
            'persons_by_films': persons_by_films,
            'news_list': news_list,
            'new_releases_list': new_releases_list,
            'top_rated_list': top_rated_list
        })
        return context


def product_detail(request, pk):
    product_list = Product.objects.select_related(
        "film__imdb_rating", "film__mpaa_rating"
    )
    product = get_object_or_404(product_list, pk=pk)
    film_info = info_by_films[pk]
    context = {
        'product': product,
        'countries': sorted(film_info['country__name']),
        'genres': sorted(film_info['genre__name']),
        'languages': sorted(film_info['language__name']),
        'distributors': sorted(film_info['distributor__name']),
        'film_persons': persons_by_films[pk]
    }
    comments = CommentToProduct.objects.filter(product=pk, is_active=True)
    initial = {'product': product.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.username
        form_class = UserCommentToProductForm
    else:
        form_class = GuestCommentToProductForm
    form = form_class(initial=initial)

    if request.method == 'POST':
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS, 'Comment added')
        else:
            form = c_form
            messages.add_message(request, messages.WARNING, 'No Comment added')

    context.update({'comments': comments, 'form': form})

    return render(request, 'cinema/product_detail.html', context)


class FilmListView(ListView):
    model = Film
    paginate_by = 8

    def get_queryset(self):
        return super().get_queryset().select_related(
            "imdb_rating", "mpaa_rating"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Movies [A-Z]',
            'info_by_films': info_by_films,
            'persons_by_films': persons_by_films
        })
        return context


class TopRatedFilmListView(FilmListView):
    ordering = "-imdb_rating__value"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Top Rated IMDb Movies',
            'criterion_name': 'IMDb Rating'
        })
        return context


class BudgetFilmListView(FilmListView):
    ordering = "-budget"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Most Expensive Movies',
            'criterion_name': 'Budget'
        })
        return context


class UsaGrossFilmListView(FilmListView):
    ordering = "-usa_gross"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Most USA Grossing Movies',
            'criterion_name': 'USA Gross'
        })
        return context


class WorldGrossFilmListView(FilmListView):
    ordering = "-world_gross"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Most Worldwide Grossing Movies',
            'criterion_name': 'World Gross'
        })
        return context


class YearFilmListView(FilmListView):
    ordering = "-imdb_rating__value"

    def get_queryset(self):
        self.requested_year = self.kwargs.get('year')
        return super().get_queryset().filter(
            release_data__year=self.requested_year
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Most Popular Movies of {self.requested_year}'
        return context


class GenreFilmListView(FilmListView):
    ordering = "-imdb_rating__value"

    def get_queryset(self):
        self.requested_genre = self.kwargs.get('genre')
        return super().get_queryset().filter(
            genre__name=self.requested_genre
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Most Popular {self.requested_genre} Movies'
        return context


class CountryFilmListView(FilmListView):
    ordering = "-imdb_rating__value"

    def get_queryset(self):
        self.requested_country = self.kwargs.get('country')
        return super().get_queryset().filter(
            country__name=self.requested_country
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Most Popular {self.requested_country} Movies'
        return context


class LanguageFilmListView(FilmListView):
    ordering = "-imdb_rating__value"

    def get_queryset(self):
        self.requested_language = self.kwargs.get('language')
        return super().get_queryset().filter(
            language__name=self.requested_language
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Most Popular Movies in ' \
                                f'{self.requested_language} '
        return context


class DistributorFilmListView(FilmListView):
    ordering = "-imdb_rating__value"

    def get_queryset(self):
        self.requested_distributor = self.kwargs.get('distributor')
        return super().get_queryset().filter(
            distributor__name=self.requested_distributor
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Most Popular Movies of " \
                                f"{self.requested_distributor}"
        return context


class MpaaFilmListView(FilmListView):
    ordering = "-imdb_rating__value"

    def get_queryset(self):
        self.requested_mpaa = self.kwargs.get('pk')
        return super().get_queryset().filter(
            mpaa_rating__pk=self.requested_mpaa
        )

    def get_context_data(self, **kwargs):
        mpaa = MpaaRating.objects.get(pk=self.requested_mpaa)
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title':
                f'Most Popular Movies with MPAA Rating of {mpaa.value}',
            'page_description': mpaa.description
        })
        return context


def film_detail(request, pk):
    film_list = Film.objects.select_related("imdb_rating", "mpaa_rating")
    film = get_object_or_404(film_list, pk=pk)
    film_info = info_by_films[pk]
    context = {
        'film': film, 'countries': sorted(film_info['country__name']),
        'genres': sorted(film_info['genre__name']),
        'languages': sorted(film_info['language__name']),
        'distributors': sorted(film_info['distributor__name']),
        'related_news': film_info['news'],
        'film_persons': persons_by_films[pk]
    }
    comments = CommentToFilm.objects.filter(film=pk, is_active=True)
    initial = {'film': film.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.username
        form_class = UserCommentToFilmForm
    else:
        form_class = GuestCommentToFilmForm
    form = form_class(initial=initial)

    if request.method == 'POST':
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS, 'Comment added')
        else:
            form = c_form
            messages.add_message(request, messages.WARNING, 'No Comment added')

    context.update({'comments': comments, 'form': form})

    return render(request, 'cinema/film_detail.html', context)


@login_required
def cinema_person_detail(request, pk):
    cinema_person_list = CinemaPerson.objects.select_related("user", "country")
    cinema_person = get_object_or_404(cinema_person_list, pk=pk)

    person_fields = ("film__genre__name", "news__pk")
    info_by_persons_qs = all_persons.values_list(
        "pk", *person_fields, "news__title", named=True
    ).order_by("-news__created_at")

    info_by_persons = {}
    for person in info_by_persons_qs:
        if person.pk not in info_by_persons:
            info_by_persons[person.pk] = {}
        for field in person_fields:
            if "news" not in info_by_persons[person.pk]:
                info_by_persons[person.pk]["news"] = {}
            if field == "film__genre__name":
                if field not in info_by_persons[person.pk]:
                    info_by_persons[person.pk][field] = []
                if person.film__genre__name not in info_by_persons[
                    person.pk][field]:
                    info_by_persons[person.pk][field].append(
                        person.film__genre__name
                    )
            elif field == "news__pk" and person.news__pk and person.news__pk \
                    not in info_by_persons[person.pk]["news"]:
                info_by_persons[person.pk]["news"][
                    person.news__pk] = person.news__title

    person_extra_info = info_by_persons[pk]

    person_professions = sorted(
        set(
            cinema_person.cinemafilmpersonprofession_set.values_list(
                "profession__name", flat=True
            )
        )
    )
    filmography = {}
    for person_profession in person_professions:
        film_info_qs = cinema_person.film_set.filter(
            cinemafilmpersonprofession__profession__name=person_profession
        ).values_list(
            "pk", "title", "release_data__year", "imdb_rating__value",
            named=True
        ).order_by("-release_data")
        filmography[person_profession] = film_info_qs

    number_of_films = []
    years_of_films = []

    for person_films in filmography.values():
        for person_film in person_films:
            number_of_films.append(person_film.pk)
            years_of_films.append(person_film.release_data__year)

    context = {
        'cinema_person': cinema_person,
        'genres': sorted(person_extra_info['film__genre__name']),
        'related_news': person_extra_info['news'],
        'person_professions': tuple(person_professions),
        'number_of_films': len(set(number_of_films)),
        'years_of_films': f'{min(years_of_films)} - {max(years_of_films)}',
        'filmography': filmography
    }
    comments = CommentToPerson.objects.filter(cinema_person=pk, is_active=True)
    initial = {'cinema_person': cinema_person.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.username
        form_class = UserCommentToPersonForm
    else:
        form_class = GuestCommentToPersonForm
    form = form_class(initial=initial)

    if request.method == 'POST':
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS, 'Comment added')
        else:
            form = c_form
            messages.add_message(request, messages.WARNING, 'No Comment added')

    context.update({'comments': comments, 'form': form})

    return render(request, 'cinema/cinema_person_detail.html', context)


class NewsListView(ListView):
    model = News
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Latest Movie News',
            'imdb_top_5': imdb_top_5,
            'budget_top_5': budget_top_5,
            'usa_gross_top_5': usa_gross_top_5,
            'world_gross_top_5': world_gross_top_5
        })
        return context


class CelebrityNewsListView(NewsListView):
    persons = CinemaPerson.objects.select_related("user").values_list(
        "user__first_name", "user__last_name", named=True
    )
    celebrities = [
        f"{person.user__first_name} {person.user__last_name}" for person in
        persons
    ]
    all_news = News.objects.values_list("pk", "title", named=True)
    news_titles = {news.pk: news.title for news in all_news}
    found_titles = []

    for pk, title in news_titles.items():
        for celebrity in celebrities:
            if celebrity in title:
                found_titles.append(pk)
                break

    def get_queryset(self):
        return super().get_queryset().filter(pk__in=self.found_titles)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Latest Celebrity News'
        return context


def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    context = {
        'news': news,
        'imdb_top_5': imdb_top_5,
        'budget_top_5': budget_top_5,
        'usa_gross_top_5': usa_gross_top_5,
        'world_gross_top_5': world_gross_top_5
    }
    comments = CommentToNews.objects.filter(news=pk, is_active=True)
    initial = {'news': news.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.username
        form_class = UserCommentToNewsForm
    else:
        form_class = GuestCommentToNewsForm
    form = form_class(initial=initial)

    if request.method == 'POST':
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS, 'Comment added')
        else:
            form = c_form
            messages.add_message(request, messages.WARNING, 'No Comment added')

    context.update({'comments': comments, 'form': form})

    return render(request, 'cinema/news_detail.html', context)


class SearchResultsView(TemplateView):
    template_name = 'cinema/search_results.html'

    def get_context_data(self, **kwargs):
        context = {}
        query = self.request.GET.get('q')
        formatted_query = ' '.join(query.strip().split())

        if formatted_query:
            product_list = Product.objects.filter(
                film__title__icontains=formatted_query
            ).select_related('film')
            film_list = Film.objects.filter(title__icontains=formatted_query)
            query_fullname = formatted_query.split()
            q = Q(user__first_name__iexact=query_fullname[:1]) & Q(
                user__last_name__iexact=query_fullname[1:]
            ) | Q(user__first_name__icontains=formatted_query) | Q(
                user__last_name__icontains=formatted_query
            )
            person_list = CinemaPerson.objects.filter(q).select_related('user')
            news_list = News.objects.filter(title__icontains=formatted_query)
            context = {
                'product_list': product_list,
                'film_list': film_list,
                'person_list': person_list,
                'news_list': news_list
            }

        context.update({
            'search_title': 'Search results for ',
            'no_results': 'No results found for ',
            'query': query,
            'imdb_top_5': imdb_top_5,
            'budget_top_5': budget_top_5,
            'usa_gross_top_5': usa_gross_top_5,
            'world_gross_top_5': world_gross_top_5
        })
        return context
