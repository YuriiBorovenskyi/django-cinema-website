from django.contrib import admin

from .models import (Country, Genre, Language, Distributor, ImdbRating,
                     MpaaRating, Film, CinemaPerson, CinemaProfession,
                     CinemaFilmPersonProfession, Product, News)


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
    list_filter = ('imdb_rating', 'mpaa_rating', 'oscar_awards')
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
    list_filter = ('gender', 'country', 'oscar_awards')
    fields = (
        'user', 'gender', 'birthday', 'country', 'bio', 'oscar_awards', 'avatar'
    )
    inlines = [CinemaFilmPersonProfessionInline]


class CinemaProfessionAdmin(admin.ModelAdmin):
    pass


class CinemaFilmPersonProfessionAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    list_display = ('film', 'price', 'in_stock', 'created_at')
    list_filter = ('price', 'in_stock')
    fields = ['film', ('price', 'in_stock'), 'created_at']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'news_source', 'news_author', 'created_at')
    list_filter = ('news_source', 'news_author')
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
