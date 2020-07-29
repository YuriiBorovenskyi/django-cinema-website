from rest_framework import serializers

from cinema.models import Film, CommentToFilm, News, CommentToNews


class FilmListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = (
            'pk', 'title', 'description', 'release_data', 'run_time',
            'budget', 'usa_gross', 'world_gross', 'oscar_awards', 'poster'
        )


class FilmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = (
            'pk', 'title', 'description', 'release_data', 'run_time',
            'budget', 'usa_gross', 'world_gross', 'oscar_awards', 'poster'
        )


class CommentToFilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentToFilm
        fields = ('film', 'author', 'content', 'created_at')


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('pk', 'title', 'description', 'created_at', 'news_source',
                  'news_author', 'news_feed_photo', 'news_detail_photo')


class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('pk', 'title', 'description', 'created_at', 'news_source',
                  'news_author', 'news_feed_photo', 'news_detail_photo')


class CommentToNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentToNews
        fields = ('news', 'author', 'content', 'created_at')
