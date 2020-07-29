from django.contrib import admin

from .models import (Country, Genre, Language, Distributor, ImdbRating,
                     MpaaRating, Film, CinemaPerson, CinemaProfession,
                     CinemaFilmPersonProfession, Product, News, CommentToPerson,
                     CommentToFilm, CommentToNews, CommentToProduct)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


class GenreAdmin(admin.ModelAdmin):
    pass


class LanguageAdmin(admin.ModelAdmin):
    pass


class DistributorAdmin(admin.ModelAdmin):
    pass


class ImdbRatingAdmin(admin.ModelAdmin):
    pass


class MpaaRatingAdmin(admin.ModelAdmin):
    pass


class CinemaFilmPersonProfessionInline(admin.TabularInline):
    model = CinemaFilmPersonProfession
    extra = 0


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0


class FilmAdmin(admin.ModelAdmin):
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


class CinemaProfessionAdmin(admin.ModelAdmin):
    pass


class CinemaFilmPersonProfessionAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    list_display = ('film', 'price', 'in_stock', 'created_at')
    list_display_links = ('film', 'price')
    list_filter = ('price', 'in_stock')
    fields = ['film', ('price', 'in_stock'), 'created_at']
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
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
    list_display = (
         'author', 'content', 'created_at', 'is_active', 'film'
    )
    list_filter = ('is_active', 'film')
    fields = ('film', 'author', 'content', 'created_at', 'is_active')


class CommentToNewsAdmin(CommentToPersonAdmin):
    list_display = (
         'author', 'content', 'created_at', 'is_active', 'news'
    )
    list_filter = ('is_active', 'news')
    fields = ('news', 'author', 'content', 'created_at', 'is_active')


class CommentToProductAdmin(CommentToPersonAdmin):
    list_display = (
         'author', 'content', 'created_at', 'is_active', 'product'
    )
    list_filter = ('is_active', 'product')
    fields = ('product', 'author', 'content', 'created_at', 'is_active')


admin.site.register(Genre, GenreAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Distributor, DistributorAdmin)
admin.site.register(ImdbRating, ImdbRatingAdmin)
admin.site.register(MpaaRating, MpaaRatingAdmin)
admin.site.register(Film, FilmAdmin)
admin.site.register(CinemaPerson, CinemaPersonAdmin)
admin.site.register(CinemaProfession, CinemaProfessionAdmin)
admin.site.register(CinemaFilmPersonProfession, CinemaFilmPersonProfessionAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CommentToPerson, CommentToPersonAdmin)
admin.site.register(CommentToFilm, CommentToFilmAdmin)
admin.site.register(CommentToNews, CommentToNewsAdmin)
admin.site.register(CommentToProduct, CommentToProductAdmin)
