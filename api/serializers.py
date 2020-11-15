from rest_framework import serializers

from cinema.models import (
    CinemaPerson,
    CommentToFilm,
    CommentToNews,
    CommentToPerson,
    Film,
    News,
)


class FilmListSerializer(serializers.ModelSerializer):
    """Serializer for getting of some data of all movies.

    It is connected with 'Film' model.
    """

    class Meta:
        model = Film
        fields = (
            "title",
            "description",
            "release_data",
            "run_time",
            "budget",
            "usa_gross",
            "world_gross",
            "oscar_awards",
            "poster",
        )


class FilmDetailSerializer(serializers.ModelSerializer):
    """Serializer for getting of some data of movie selected by visitor.

    It is connected with 'Film' model.
    """

    class Meta:
        model = Film
        fields = (
            "title",
            "description",
            "release_data",
            "run_time",
            "budget",
            "usa_gross",
            "world_gross",
            "oscar_awards",
            "poster",
        )


class CommentToFilmSerializer(serializers.ModelSerializer):
    """Serializer for getting of comments to movie selected by visitor.

    Also it adds new comment to movie. It is connected with
    'CommentToFilm' model.
    """

    class Meta:
        model = CommentToFilm
        fields = ("film", "author", "content", "created_at")


class NewsListSerializer(serializers.ModelSerializer):
    """Serializer for getting of some data of all cinema news.

    It is connected with 'News' model.
    """

    class Meta:
        model = News
        fields = (
            "title",
            "description",
            "created_at",
            "news_source",
            "news_author",
            "news_feed_photo",
            "news_detail_photo",
        )


class NewsDetailSerializer(serializers.ModelSerializer):
    """Serializer for getting of some data of cinema news selected by visitor.

    It is connected with 'News' model.
    """

    class Meta:
        model = News
        fields = (
            "title",
            "description",
            "created_at",
            "news_source",
            "news_author",
            "news_feed_photo",
            "news_detail_photo",
        )


class CommentToNewsSerializer(serializers.ModelSerializer):
    """Serializer for getting of comments to cinema news selected by visitor.

    Also it adds new comment to cinema news. It is connected with
    'CommentToNews' model.
    """

    class Meta:
        model = CommentToNews
        fields = ("news", "author", "content", "created_at")


class CinemaPersonDetailSerializer(serializers.ModelSerializer):
    """Serializer for getting of some data of cinema person selected by
    visitor.

    It is connected with 'CinemaPerson' model.
    """

    class Meta:
        model = CinemaPerson
        fields = (
            "fullname",
            "gender",
            "birthday",
            "bio",
            "oscar_awards",
            "avatar",
        )


class CommentToPersonSerializer(serializers.ModelSerializer):
    """Serializer for getting of comments to cinema person selected by visitor.

    Also it adds new comment to cinema person. It is connected with
    'CommentToPerson' model.
    """

    class Meta:
        model = CommentToPerson
        fields = ("cinema_person", "author", "content", "created_at")
