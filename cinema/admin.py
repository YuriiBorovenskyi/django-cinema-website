from django.contrib import admin

from .models import (
    Country, Genre, Language, Distributor, ImdbRating, MpaaRating, Film,
    CinemaPerson, CinemaProfession, CinemaFilmPersonProfession, Product,
    News, CommentToPerson, CommentToFilm, CommentToNews, CommentToProduct
)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """
    Editor of 'Country' model.

    Set parameters of 'Country' model view in interface of admin site Django.
    """
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Editor of 'Genre' model.

    Set parameters of 'Genre' model view in interface of admin site Django.
    """
    pass


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    """
    Editor of 'Language' model.

    Set parameters of 'Language' model view in interface of admin site Django.
    """
    pass


@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
    """
    Editor of 'Distributor' model.

    Set parameters of 'Distributor' model view in interface of admin site
    Django.
    """
    pass


@admin.register(ImdbRating)
class ImdbRatingAdmin(admin.ModelAdmin):
    """
    Editor of 'ImdbRating' model.

    Set parameters of 'ImdbRating' model view in interface of admin site Django.
    """
    pass


@admin.register(MpaaRating)
class MpaaRatingAdmin(admin.ModelAdmin):
    """
    Editor of 'MpaaRating' model.

    Set parameters of 'MpaaRating' model view in interface of admin site Django.
    """
    pass


class CinemaFilmPersonProfessionInline(admin.TabularInline):
    """
    Built-in editor of 'CinemaFilmPersonProfession' model.

    Add related records of 'CinemaFilmPersonProfession' model to web page
    display / edit of 'Film' model in interface of admin site Django.
    """
    model = CinemaFilmPersonProfession


class ProductInline(admin.TabularInline):
    """
    Built-in editor of 'Product' model.

    Add related records of 'Product' model to web page display / edit of
    'Film' model in interface of admin site Django.
    """
    model = Product


class FilmAdmin(admin.ModelAdmin):
    """
    Editor of 'Film' model.

    Set parameters of 'Film' model view in interface of admin site Django.
    """
    list_display = (
        'title', 'year', 'run_time', 'budget', 'usa_gross', 'world_gross',
        'imdb_rating', 'mpaa_rating', 'oscar_awards'
    )
    list_display_links = ('title', 'year', 'run_time',)
    list_filter = ('imdb_rating', 'mpaa_rating', 'oscar_awards')
    search_fields = ('title', 'description')
    fieldsets = (
        ('IMDb Main', {
            'fields': ('title', 'run_time', 'release_data', 'imdb_rating')
        }),
        ('IMDb Extra', {
            'fields': ('genre', 'mpaa_rating', 'country', 'language')
        }),
        ('IMDb Box Office', {
            'fields': ('budget', 'usa_gross', 'world_gross')
        }),
        ('Wiki', {
            'fields': ('description', 'oscar_awards', 'distributor')
        }),
        ('Media', {
            'fields': ('poster',)
        }),
    )
    inlines = [CinemaFilmPersonProfessionInline, ProductInline]


class CinemaPersonAdmin(admin.ModelAdmin):
    """
    Editor of 'CinemaPerson' model.

    Set parameters of 'CinemaPerson' model view in interface of admin site
    Django.
    """
    list_display = (
        'fullname', 'gender', 'country', 'birthday', 'oscar_awards'
    )
    list_display_links = ('fullname', 'birthday')
    list_filter = ('gender', 'country', 'oscar_awards')
    search_fields = ('bio',)
    fields = (
        'user', 'gender', 'birthday', 'country', 'bio', 'oscar_awards', 'avatar'
    )
    inlines = [CinemaFilmPersonProfessionInline]
    date_hierarchy = 'birthday'


@admin.register(CinemaProfession)
class CinemaProfessionAdmin(admin.ModelAdmin):
    """
    Editor of 'CinemaProfession' model.

    Set parameters of 'CinemaProfession' model view in interface of admin site
    Django.
    """
    pass


@admin.register(CinemaFilmPersonProfession)
class CinemaFilmPersonProfessionAdmin(admin.ModelAdmin):
    """
    Editor of 'CinemaFilmPersonProfession' model.

    Set parameters of 'CinemaFilmPersonProfession' model view in interface of
    admin site Django.
    """
    pass


class ProductAdmin(admin.ModelAdmin):
    """
    Editor of 'Product' model.

    Set parameters of 'Product' model view in interface of admin site Django.
    """
    list_display = ('film', 'price', 'in_stock', 'created_at')
    list_display_links = ('film', 'price')
    list_filter = ('price', 'in_stock')
    fields = ['film', ('price', 'in_stock'), 'created_at']
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)


class NewsAdmin(admin.ModelAdmin):
    """
    Editor of 'News' model.

    Set parameters of 'News' model view in interface of admin site Django.
    """
    list_display = ('title', 'news_source', 'news_author', 'created_at')
    list_display_links = ('title', 'news_source', 'news_author')
    list_filter = ('news_source', 'news_author')
    search_fields = ('title', 'news_source', 'news_author')
    fieldsets = (
        ('Main', {
            'fields': ('title', 'description', 'created_at')
        }),
        ('Source Details', {
            'fields': ('news_source', 'news_author')
        }),
        ('Related Info', {
            'fields': ('film', 'cinema_person')
        }),
        ('Media', {
            'fields': ('news_feed_photo', 'news_detail_photo')
        }),
    )
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)


class CommentToPersonAdmin(admin.ModelAdmin):
    """
    Editor of 'CommentToPerson' model.

    Set parameters of 'CommentToPerson' model view in interface of admin site
    Django.
    """
    list_display = (
         'author', 'content', 'created_at', 'is_active', 'cinema_person'
    )
    list_display_links = ('author', 'content')
    list_filter = ('is_active', 'cinema_person')
    search_fields = ('author', 'content')
    date_hierarchy = 'created_at'
    fields = ('cinema_person', 'author', 'content', 'created_at', 'is_active')
    readonly_fields = ('created_at',)


class CommentToFilmAdmin(CommentToPersonAdmin):
    """
    Editor of 'CommentToFilm' model.

    Set parameters of 'CommentToFilm' model view in interface of admin site
    Django.
    """
    list_display = (
         'author', 'content', 'created_at', 'is_active', 'film'
    )
    list_filter = ('is_active', 'film')
    fields = ('film', 'author', 'content', 'created_at', 'is_active')


class CommentToNewsAdmin(CommentToPersonAdmin):
    """
    Editor of 'CommentToNews' model.

    Set parameters of 'CommentToNews' model view in interface of admin site
    Django.
    """
    list_display = (
         'author', 'content', 'created_at', 'is_active', 'news'
    )
    list_filter = ('is_active', 'news')
    fields = ('news', 'author', 'content', 'created_at', 'is_active')


class CommentToProductAdmin(CommentToPersonAdmin):
    """
    Editor of 'CommentToProduct' model.

    Set parameters of 'CommentToProduct' model view in interface of admin
    site Django.
    """
    list_display = (
         'author', 'content', 'created_at', 'is_active', 'product'
    )
    list_filter = ('is_active', 'product')
    fields = ('product', 'author', 'content', 'created_at', 'is_active')


admin.site.register(Film, FilmAdmin)
admin.site.register(CinemaPerson, CinemaPersonAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(CommentToPerson, CommentToPersonAdmin)
admin.site.register(CommentToFilm, CommentToFilmAdmin)
admin.site.register(CommentToNews, CommentToNewsAdmin)
admin.site.register(CommentToProduct, CommentToProductAdmin)
