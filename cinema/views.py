import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, TemplateView

from .forms import (
    UserCommentToProductForm,
    GuestCommentToProductForm,
    UserCommentToFilmForm,
    GuestCommentToFilmForm,
    UserCommentToPersonForm,
    GuestCommentToPersonForm,
    UserCommentToNewsForm,
    GuestCommentToNewsForm,
)
from .models import (
    Product,
    News,
    Film,
    CinemaPerson,
    MpaaRating,
)
from .services import (
    get_cast_and_crew,
    get_films_info,
    get_persons_info,
    get_films_ratings_sets,
    get_celebrity_news_id,
    get_filmography_and_extra_info,
)

DESCRIPTION_BLU_RAY = "Welcome to the fantastic Blu-ray department here, " \
                      "where you can find the films, you could ever want to " \
                      "see in superb high definition quality. We're " \
                      "constantly adding all of the latest Blu-ray releases " \
                      "to our collection and always have an unbelievable " \
                      "offer or two. We promise great deals on the best films!"
DESCRIPTION_NEWS = "The latest movie news on the movies 'you're most " \
                   "interested in seeing."

films_cast_and_crew = get_cast_and_crew()
films_info = get_films_info()
persons_info = get_persons_info()
films_ratings_sets = get_films_ratings_sets()
celebrity_news_id = get_celebrity_news_id()


class ProductListView(ListView):
    """
    Display page with list of blue-ray movies.
    """
    paginate_by = 8
    queryset = Product.products.order_by_name()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Movies on Blu-ray',
            'films_cast_and_crew': films_cast_and_crew
        })
        return context


class TopRatedProductListView(ProductListView):
    """
    Display page with list of top rated blue-ray movies.
    """
    ordering = "-film__imdb_rating__value"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Top Rated Movies on Blu-ray'
        return context


class NewReleasesProductListView(ProductListView):
    """
    Display page with list of new releases blue-ray movies.
    """
    ordering = "-film__release_data"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'New Releases Movies on Blu-ray'
        return context


class IndexView(TemplateView):
    """
    Display home page of website.
    """
    template_name = 'cinema/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_rated_products = Product.products.order_by_imdb_rating()
        new_releases_products = Product.products.order_by_release_data()
        news_list = News.objects.all()
        context.update({
            'page_title': "Latest Movie News, Movies on Blu-ray",
            'title_news': "Cinema News",
            'description_news': DESCRIPTION_NEWS,
            'title_blu_ray': "Movies on Blu-ray",
            'description_blu_ray': DESCRIPTION_BLU_RAY,
            'title_top_rated': 'Top Rated',
            'title_new_releases': 'New Releases',
            'films_cast_and_crew': films_cast_and_crew,
            'news_list': news_list,
            'new_releases_products': new_releases_products,
            'top_rated_products': top_rated_products
        })
        return context


def product_detail(request, pk):
    """
    Display page with details of blue-ray movie selected by visitor.

    Also display comments to blue-ray movie and form for adding new comment.
    Create "CommentToProduct" model record.
    After saving data, redirect to current page.
    """
    product_list = Product.products.all()
    product = get_object_or_404(product_list, pk=pk)
    context = {
        'product': product,
        'film_info': films_info[pk],
        'film_cast_and_crew': films_cast_and_crew[pk]
    }
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

    context['form'] = form

    return render(request, 'cinema/product_detail.html', context)


class FilmListView(ListView):
    """
    Display page with list of movies.
    """
    paginate_by = 8
    queryset = Film.films.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Movies [A-Z]',
            'films_info': films_info,
            'films_cast_and_crew': films_cast_and_crew
        })
        return context


class TopRatedFilmListView(FilmListView):
    """
    Display page with list of top rated movies.
    """
    ordering = "-imdb_rating__value"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Top Rated IMDb Movies',
            'criterion_name': 'IMDb Rating'
        })
        return context


class BudgetFilmListView(FilmListView):
    """
    Display page with list of most expensive movies.
    """
    ordering = "-budget"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Most Expensive Movies',
            'criterion_name': 'Budget'
        })
        return context


class UsaGrossFilmListView(FilmListView):
    """
    Display page with list of most USA grossing movies.
    """
    ordering = "-usa_gross"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Most USA Grossing Movies',
            'criterion_name': 'USA Gross'
        })
        return context


class WorldGrossFilmListView(FilmListView):
    """
    Display page with list of most worldwide grossing movies.
    """
    ordering = "-world_gross"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Most Worldwide Grossing Movies',
            'criterion_name': 'World Gross'
        })
        return context


class YearFilmListView(FilmListView):
    """
    Display page with list of most popular movies, that are related to
    selected year by visitor.
    """

    def get_queryset(self):
        self.requested_year = self.kwargs.get('year')
        return Film.films.filter_by_selected_year(self.requested_year)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Most Popular Movies of {self.requested_year}'
        return context


class GenreFilmListView(FilmListView):
    """
    Display page with list of most popular movies, that are related to
    selected genre by visitor.
    """

    def get_queryset(self):
        self.requested_genre = self.kwargs.get('genre')
        return Film.films.filter_by_selected_genre(
            self.requested_genre
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Most Popular {self.requested_genre} Movies'
        return context


class CountryFilmListView(FilmListView):
    """
    Display page with list of most popular movies, that are related to
    selected country by visitor.
    """

    def get_queryset(self):
        self.requested_country = self.kwargs.get('country')
        return Film.films.filter_by_selected_country(
            self.requested_country
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Most Popular {self.requested_country} Movies'
        return context


class LanguageFilmListView(FilmListView):
    """
    Display page with list of most popular movies, that are related to
    selected language by visitor.
    """

    def get_queryset(self):
        self.requested_language = self.kwargs.get('language')
        return Film.films.filter_by_selected_language(
            self.requested_language
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Most Popular Movies in ' \
                                f'{self.requested_language} '
        return context


class DistributorFilmListView(FilmListView):
    """
    Display page with list of most popular movies, that are related to
    selected distributor by visitor.
    """

    def get_queryset(self):
        self.requested_distributor = self.kwargs.get('distributor')
        return Film.films.filter_by_selected_distributor(
            self.requested_distributor
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Most Popular Movies of " \
                                f"{self.requested_distributor}"
        return context


class MpaaFilmListView(FilmListView):
    """
    Display page with list of most popular movies, that are related to
    selected MPAA rating by visitor.
    """

    def get_queryset(self):
        self.requested_mpaa = self.kwargs.get('pk')
        return Film.films.filter_by_selected_mpaa_rating(
            self.requested_mpaa
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
    """
    Display page with details of movie selected by visitor.

    Also display comments to movie and form for adding new comment.
    Create "CommentToFilm" model record.
    After saving data, redirect to current page.
    """
    film_list = Film.films.all()
    film = get_object_or_404(film_list, pk=pk)
    context = {
        'film': film,
        'film_info': films_info[pk],
        'film_cast_and_crew': films_cast_and_crew[pk]
    }
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

    context['form'] = form

    return render(request, 'cinema/film_detail.html', context)


@login_required
def cinema_person_detail(request, pk):
    """
    Display page with details of cinema person selected by visitor.

    Also display comments to cinema person and form for adding new comment.
    Create "CommentToPerson" model record.
    After saving data, redirect to current page.

    Only signed-in users will be allowed to access this web page.
    """
    cinema_person_list = CinemaPerson.persons.all()
    cinema_person = get_object_or_404(cinema_person_list, pk=pk)
    filmography, person_professions, films_number, films_years_range = \
        get_filmography_and_extra_info(cinema_person)

    context = {
        'cinema_person': cinema_person,
        'person_info': persons_info[pk],
        'person_professions': person_professions,
        'films_number': films_number,
        'films_years_range': films_years_range,
        'filmography': filmography
    }
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

    context['form'] = form

    return render(request, 'cinema/cinema_person_detail.html', context)


class NewsListView(ListView):
    """
    Display page with list of latest cinema news.
    """
    model = News
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Latest Movie News',
            'imdb_top_5': films_ratings_sets['imdb_rating__value'],
            'budget_top_5': films_ratings_sets['budget'],
            'usa_gross_top_5': films_ratings_sets['usa_gross'],
            'world_gross_top_5': films_ratings_sets['world_gross'],
        })
        return context


class CelebrityNewsListView(NewsListView):
    """
    Display page with list of latest cinema news about celebrities.
    """
    queryset = News.news.get_news_about_celebrities(celebrity_news_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Latest Celebrity News'
        return context


def news_detail(request, pk):
    """
    Display page with details of cinema news selected by visitor.

    Also display comments to news and form for adding new comment.
    Create "CommentToNews" model record.
    After saving data, redirect to current page.
    """
    news = get_object_or_404(News, pk=pk)
    context = {
        'news': news,
        'imdb_top_5': films_ratings_sets['imdb_rating__value'],
        'budget_top_5': films_ratings_sets['budget'],
        'usa_gross_top_5': films_ratings_sets['usa_gross'],
        'world_gross_top_5': films_ratings_sets['world_gross'],
    }
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

    context['form'] = form

    return render(request, 'cinema/news_detail.html', context)


class SearchResultsView(TemplateView):
    """
    Displays page with search results for website.
    """
    template_name = 'cinema/search_results.html'

    def get_context_data(self, **kwargs):
        context = {}
        search_word = self.request.GET.get('q')
        cleaned_search_word = re.sub(r'\s+', ' ', search_word.strip())

        if cleaned_search_word:
            product_list = Product.products.filter_by_search_word(
                cleaned_search_word
            )
            film_list = Film.films.filter_by_search_word(
                cleaned_search_word
            )
            person_list = CinemaPerson.persons.filter_by_search_word(
                cleaned_search_word
            )
            news_list = News.news.filter_by_search_word(
                cleaned_search_word
            )
            context = {
                'product_list': product_list,
                'film_list': film_list,
                'person_list': person_list,
                'news_list': news_list
            }

        context.update({
            'search_title': 'Search results for ',
            'no_results': 'No results found for ',
            'search_word': search_word,
            'imdb_top_5': films_ratings_sets['imdb_rating__value'],
            'budget_top_5': films_ratings_sets['budget'],
            'usa_gross_top_5': films_ratings_sets['usa_gross'],
            'world_gross_top_5': films_ratings_sets['world_gross'],
        })
        return context
