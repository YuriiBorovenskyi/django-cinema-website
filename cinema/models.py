from datetime import date, timedelta

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Prefetch, Q
from django.db.models.signals import post_save

from accounts.models import User
from .tasks import send_new_product_notification

GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
)


def upload_to_film(instance, filename):
    """
    Get path in format string to media file for field 'poster' of
    'Film' model.
    """
    return "films/{}_{}.jpg".format(instance.title, instance.pk)


def upload_to_cinema_person(instance, filename):
    """
    Get path in format string to media file for field 'avatar' of
    'CinemaPerson' model.
    """
    return "cinema_persons/{}_{}_{}.jpg".format(
        instance.user.first_name, instance.user.last_name, instance.pk
    )


def upload_photo_to_news_feed(instance, filename):
    """
    Get path in format string to media file for field 'news_feed_photo'
    of 'News' model.
    """
    return "cinema_news_feed/{}_{}.jpg".format(instance.title, instance.pk)


def upload_photo_to_news_detail(instance, filename):
    """
    Get path in format string to media file for field 'news_detail_photo'
    of 'News' model.
    """
    return "cinema_news_detail/{}_{}.jpg".format(instance.title, instance.pk)


class ExtendedProfileMixin(models.Model):
    """
    Mixin model, what extends 'CinemaPerson' model.
    """
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="M")
    country = models.ForeignKey("Country", on_delete=models.PROTECT, default=1)
    birthday = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True


class DateMixin(models.Model):
    """
    Mixin model, what extends other models: Product, News, Comment...
    """
    created_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class Country(models.Model):
    """
    Save country data needed for 'Film' and 'CinemaPerson' models.
    """
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ["name"]


class Genre(models.Model):
    """
    Save genre data needed for 'Film' model.
    """
    name = models.CharField(
        max_length=16, unique=True, validators=[
            RegexValidator(
                regex="^[A-Z][a-z]+[-]?[a-z]+$",
                message="Invalid genre name format.",
                code="invalid"
            )
        ]
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class ImdbRating(models.Model):
    """
    Save imdb rating data needed for 'Film' model.
    """
    value = models.DecimalField(max_digits=2, decimal_places=1, unique=True)

    def __str__(self):
        return str(self.value)

    class Meta:
        ordering = ["value"]


class MpaaRating(models.Model):
    """
    Save mpaa rating data needed for 'Film' model.
    """
    value = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=512, unique=True)

    def __str__(self):
        return str(self.value)

    class Meta:
        ordering = ["value"]


class Language(models.Model):
    """
    Save language data needed for 'Film' model.
    """
    name = models.CharField(
        max_length=16, unique=True, validators=[
            RegexValidator(
                regex="^[A-Z][a-z]+$",
                message="Invalid language name format.",
                code="invalid"
            )
        ]
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Distributor(models.Model):
    """
    Save distributor data needed for 'Film' model.
    """
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class CinemaPersonManager(models.Manager):
    """
    Custom Manager, adding extra manager methods.

    Custom Manager used in 'CinemaPerson' model by extending base Manager class
    and instantiating custom Manager in 'CinemaPerson' model.
    """
    def all(self):
        """
        Return QuerySet object with cached data of some related models.
        """
        return super().get_queryset().select_related("user", "country")

    def get_brief_data(self):
        """
        Return QuerySet object with data of specified fields of
        'CinemaPerson' and 'User' models.
        """
        return super().get_queryset().select_related("user").values_list(
            "pk", "user__first_name",  "user__last_name", named=True
        )

    def filter_by_search_word(self, search_words):
        """
        Return QuerySet object, value of selected field corresponds to
        search word entered by visitor.
        """
        separate_search_words = search_words.split()
        q = (Q(user__first_name__istartswith=separate_search_words[0]) &
             Q(user__last_name__iendswith=separate_search_words[-1])) | Q(
            user__first_name__icontains=search_words) | Q(
            user__last_name__icontains=search_words
        )
        return self.all().filter(q)

    def get_cached_data(self):
        """
        Return QuerySet object with cached data of all related models.
        """
        return self.all().prefetch_related(
            "news_set", "film_set__genre",
            Prefetch("film_set", Film.objects.select_related("imdb_rating"))
        )

    def get_related_data(self, fields_names):
        """
        Return QuerySet object with data of specified fields of
        'CinemaPerson' model and some related models.
        """
        return self.get_cached_data().values_list(
            "pk", *fields_names, "news__title", named=True
        ).order_by("-news__created_at")


class CinemaPerson(ExtendedProfileMixin):
    """
    Save data about actors, directors, writers needed for 'Film' model.

    Model related with next models:
    - User (one-to-one relationship);
    - Film, News (many-to-many relationship);
    - CommentToPerson (many-to-one relationship).

    Class of this model inherits from 'ExtendedProfileMixin' class.
    """
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    bio = models.TextField()
    oscar_awards = models.PositiveSmallIntegerField(default=0)
    avatar = models.ImageField(
        upload_to=upload_to_cinema_person, blank=True, null=True
    )
    objects = models.Manager()
    persons = CinemaPersonManager()

    @property
    def age(self):
        """
        Get information about age of actors, directors, writers.
        """
        if self.birthday:
            return (date.today() - self.birthday) // timedelta(days=365.2425)
        return None

    @property
    def fullname(self):
        """
        Get fullname of actors, directors, writers.
        """
        return f"{self.user.get_full_name()}"

    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ["user__first_name", "user__last_name"]


class FilmManager(models.Manager):
    """
    Custom Manager, adding extra manager methods.

    Custom Manager used in 'Film' model by extending base Manager class
    and instantiating custom Manager in 'Film' model.
    """
    def all(self):
        """
        Return QuerySet object with cached data of some related models.
        """
        return super().get_queryset().select_related(
            "imdb_rating", "mpaa_rating", "product"
        )

    def get_brief_data(self):
        """
        Return QuerySet object with data of specified fields of 'Film' model.
        """
        return super().get_queryset().values_list("pk", "title", named=True)

    def filter_by_selected_year(self, selected_year):
        """
        Return QuerySet object filtered by selected year and order by
        imdb rating of movies.
        """
        return self.all().filter(
            release_data__year=selected_year
        ).order_by("-imdb_rating__value")

    def filter_by_selected_genre(self, selected_genre):
        """
        Return QuerySet object filtered by selected genre and order by
        imdb rating of movies.
        """
        return self.all().filter(
            genre__name=selected_genre
        ).order_by("-imdb_rating__value")

    def filter_by_selected_country(self, selected_country):
        """
        Return QuerySet object filtered by selected country and order by
        imdb rating of movies.
        """
        return self.all().filter(
            country__name=selected_country
        ).order_by("-imdb_rating__value")

    def filter_by_selected_language(self, selected_language):
        """
        Return QuerySet object filtered by selected language and order by
        imdb rating of movies.
        """
        return self.all().filter(
            language__name=selected_language
        ).order_by("-imdb_rating__value")

    def filter_by_selected_distributor(self, selected_distributor):
        """
        Return QuerySet object filtered by selected distributor and order by
        imdb rating of movies.
        """
        return self.all().filter(
            distributor__name=selected_distributor
        ).order_by("-imdb_rating__value")

    def filter_by_selected_mpaa_rating(self, selected_mpaa_rating):
        """
        Return QuerySet object filtered by selected MPAA rating and order by
        imdb rating of movies.
        """
        return self.all().filter(
            mpaa_rating__pk=selected_mpaa_rating
        ).order_by("-imdb_rating__value")

    def filter_by_search_word(self, search_word):
        """
        Return QuerySet object, value of selected field corresponds to
        search word entered by visitor.
        """
        return self.all().filter(title__icontains=search_word)

    def get_cached_data(self):
        """
        Return QuerySet object with cached data of all related models.
        """
        return self.all().prefetch_related(
            "country", "genre", "language", "distributor", "news_set",
            "staff__user", Prefetch(
                "staff__cinemafilmpersonprofession_set",
                queryset=CinemaFilmPersonProfession.objects.select_related(
                    "profession"
                )
            )
        )

    def get_related_data(self, fields_names):
        """
        Return QuerySet object with data of specified fields of 'Film'
        model and some related models.
        """
        return self.get_cached_data().values_list(
            "pk", *fields_names, "news__title", named=True
        ).order_by("-news__created_at")


class Film(models.Model):
    """
    The most main model storing film data.

    Model related with next models:
    - Product (one-to-one relationship);
    - Country, Genre, CinemaPerson, News, Language, Distributor
    (many-to-many relationship);
    - ImdbRating, MpaaRating, CommentToFilm (many-to-one relationship).
    """
    title = models.CharField(max_length=64, db_index=True)
    country = models.ManyToManyField(Country)
    genre = models.ManyToManyField(Genre)
    staff = models.ManyToManyField(
        CinemaPerson, through="CinemaFilmPersonProfession"
    )
    budget = models.PositiveIntegerField(null=True, blank=True)
    usa_gross = models.PositiveIntegerField(default=0)
    world_gross = models.PositiveIntegerField(default=0)
    run_time = models.DurationField()
    description = models.TextField()
    release_data = models.DateField()
    language = models.ManyToManyField(Language)
    distributor = models.ManyToManyField(Distributor)
    imdb_rating = models.ForeignKey(ImdbRating, on_delete=models.PROTECT)
    mpaa_rating = models.ForeignKey(
        MpaaRating, on_delete=models.PROTECT, default=1
    )
    oscar_awards = models.PositiveSmallIntegerField(default=0)
    poster = models.ImageField(upload_to=upload_to_film, blank=True, null=True)

    objects = models.Manager()
    films = FilmManager()

    def __str__(self):
        return self.title

    @property
    def year(self):
        """
        Get information about year when film was released.
        """
        return self.release_data.year

    class Meta:
        ordering = ["title"]


class CinemaProfession(models.Model):
    """
    Save profession name for cinema persons who took part in film.
    """
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["pk"]


class CinemaFilmPersonProfession(models.Model):
    """
    Intermediate relation model.

    Related 'Film' and 'CinemaPerson' models by many-to-many relationship.
    Has additional field which keeps profession of cinema persons.
    """
    cinema_person = models.ForeignKey(CinemaPerson, on_delete=models.PROTECT)
    film = models.ForeignKey(Film, on_delete=models.PROTECT)
    profession = models.ForeignKey(
        CinemaProfession, on_delete=models.PROTECT, default=2
    )

    def __str__(self):
        return (
            f"{self.film.title}: {self.profession.name} - "
            f"{self.cinema_person.fullname}"
        )

    class Meta:
        verbose_name = "Cinema film person profession"
        verbose_name_plural = "Cinema films persons professions"
        ordering = ["film__title", "profession",
                    "cinema_person__user__first_name"]


class NewsManager(models.Manager):
    """
    Custom Manager, adding extra manager methods.

    Custom Manager used in 'News' model by extending base Manager class
    and instantiating custom Manager in 'News' model.
    """
    def get_brief_data(self):
        """
        Return QuerySet object with data of specified fields of 'News' model.
        """
        return super().get_queryset().values_list("pk", "title", named=True)

    def get_news_about_celebrities(self, celebrity_news_id):
        """
        Return QuerySet object with news data about celebrities.
        """
        return super().get_queryset().filter(pk__in=celebrity_news_id)

    def filter_by_search_word(self, search_word):
        """
        Return QuerySet object, value of selected field corresponds to
        search word entered by visitor.
        """
        return super().get_queryset().filter(title__icontains=search_word)


class News(DateMixin):
    """
    Save news data about world cinema.

    Model related with next models:
    - Film, CinemaPerson (many-to-many relationship);
    - CommentToNews (many-to-one relationship).

    Class of this model inherits from 'DateMixin' class.
    """
    title = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    news_source = models.CharField(max_length=32)
    news_author = models.CharField(max_length=64)
    film = models.ManyToManyField(Film, blank=True)
    cinema_person = models.ManyToManyField(CinemaPerson, blank=True)
    news_feed_photo = models.ImageField(
        upload_to=upload_photo_to_news_feed, blank=True, null=True
    )
    news_detail_photo = models.ImageField(
        upload_to=upload_photo_to_news_detail, blank=True, null=True
    )
    objects = models.Manager()
    news = NewsManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "News"
        ordering = ["-created_at"]


class ProductManager(models.Manager):
    """
    Custom Manager, adding extra manager methods.

    Custom Manager used in 'Product' model by extending base Manager class
    and instantiating custom Manager in 'Product' model.
    """
    def all(self):
        """
        Return QuerySet object with cached data of related models.
        """
        return super().get_queryset().select_related(
            "film", "film__imdb_rating", "film__mpaa_rating"
        )

    def order_by_name(self):
        """
        Return QuerySet object containing only 'Product' model data and
        order by name of blu-ray movies.
        """
        return self.all().only("pk", "price", "film", "in_stock")

    def order_by_imdb_rating(self):
        """
        Return QuerySet object containing only 'Product' model data and
        order by imdb rating of blu-ray movies.
        """
        return self.all().only(
            "pk", "price", "film", "in_stock"
        ).order_by("-film__imdb_rating__value")

    def order_by_release_data(self):
        """
        Return QuerySet object containing only 'Product' model data and
        order by release date of blu-ray movies.
        """
        return self.all().only(
            "pk", "price", "film", "in_stock"
        ).order_by("-film__release_data")

    def filter_by_search_word(self, search_word):
        """
        Return QuerySet object, value of selected field corresponds to
        search word entered by visitor.
        """
        return self.all().filter(film__title__icontains=search_word)


class Product(DateMixin):
    """
    Save information about movies on blu-ray.

    Model related with next models:
    - Film (one-to-one relationship);
    - CommentToProduct (many-to-one relationship).

    Class of this model inherits from 'DateMixin' class.
    """
    price = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0.99)], error_messages={
            "min_value": "Product price cannot be less than 0.99."
        }
    )
    in_stock = models.PositiveSmallIntegerField(default=0)
    film = models.OneToOneField(Film, on_delete=models.CASCADE)

    objects = models.Manager()
    products = ProductManager()

    def __str__(self):
        return f"{self.film.title} [Blu-ray]"

    class Meta:
        ordering = ["film__title", ]


class CommentMixin(models.Model):
    """
    Mixin model, what extends Comments models.
    """
    author = models.CharField(max_length=32)
    content = models.TextField()
    is_active = models.BooleanField(default=True, db_index=True,
                                    verbose_name='Display on screen?')

    class Meta:
        abstract = True


class CommentToPerson(CommentMixin, DateMixin):
    """
    Save comments to actors, directors, writers.

    Class of this model inherits from 'CommentMixin' and 'DateMixin' classes.
    """
    cinema_person = models.ForeignKey(CinemaPerson, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Comments to persons'
        ordering = ["-created_at"]


class CommentToFilm(CommentMixin, DateMixin):
    """
    Save comments to movies.

    Class of this model inherits from 'CommentMixin' and 'DateMixin' classes.
    """
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Comments to films'
        ordering = ["-created_at"]


class CommentToNews(CommentMixin, DateMixin):
    """
    Save comments to cinema news.

    Class of this model inherits from 'CommentMixin' and 'DateMixin' classes.
    """
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Comments to news'
        ordering = ["-created_at"]


class CommentToProduct(CommentMixin, DateMixin):
    """
    Save comments to movies on blu-ray.

    Class of this model inherits from 'CommentMixin' and 'DateMixin' classes.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Comments to products'
        ordering = ["-created_at"]


def post_save_dispatcher(sender, instance, created, **kwargs):
    """
    Signal handler function.

    After saving record of 'Product' model in database, 'post_save' signal
    will be send, which calls this signal handler.
    Call function that sends notification messages to registered users about
    appearance of new movie on blu-ray.

    'send_new_product_notification' is celery task that will run in task
    queue (keeps in redis) and launch in background.
    """
    if created:
        send_new_product_notification.delay(instance.pk)


post_save.connect(post_save_dispatcher, sender=Product)
