from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from cinema.models import (
    Film, CommentToFilm,
    News, CommentToNews,
    CinemaPerson, CommentToPerson,
)
from .serializers import (
    FilmListSerializer,
    FilmDetailSerializer,
    CommentToFilmSerializer,
    NewsListSerializer,
    NewsDetailSerializer,
    CommentToNewsSerializer,
    CinemaPersonDetailSerializer,
    CommentToPersonSerializer,
)


class FilmListView(ListAPIView):
    """
    Display data of all movies in 'JSON' and 'API' formats.
    """
    queryset = Film.objects.order_by('pk')
    serializer_class = FilmListSerializer


class FilmDetailView(RetrieveAPIView):
    """
    Display data of movie selected by visitor in 'JSON' and 'API' formats.
    """
    queryset = Film.objects.all()
    serializer_class = FilmDetailSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def comments_to_film(request, pk):
    """
    Display comments to movie selected by visitor in 'JSON' and 'API' formats.

    Add new comment to movie.
    Create "CommentToFilm" model record and save it in DB.

    Only signed-in users will be allowed access to add comment.
    """
    if request.method == 'POST':
        serializer = CommentToFilmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        comments = CommentToFilm.objects.filter(is_active=True, film=pk)
        serializer = CommentToFilmSerializer(comments, many=True)
        return Response(serializer.data)


class NewsListView(ListAPIView):
    """
    Display data of all cinema news in 'JSON' and 'API' formats.
    """
    queryset = News.objects.order_by('pk')
    serializer_class = NewsListSerializer


class NewsDetailView(RetrieveAPIView):
    """
    Display data of news selected by visitor in 'JSON' and 'API' formats.
    """
    queryset = News.objects.all()
    serializer_class = NewsDetailSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def comments_to_news(request, pk):
    """
    Display comments to news selected by visitor in 'JSON' and 'API' formats.

    Add new comment to cinema news.
    Create "CommentToNews" model record and save it in DB.

    Only signed-in users will be allowed access to add comment.
    """
    if request.method == 'POST':
        serializer = CommentToNewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        comments = CommentToNews.objects.filter(is_active=True, news=pk)
        serializer = CommentToNewsSerializer(comments, many=True)
        return Response(serializer.data)


class CinemaPersonDetailView(RetrieveAPIView):
    """
    Display data of person selected by visitor in 'JSON' and 'API' formats.
    """
    queryset = CinemaPerson.objects.all()
    serializer_class = CinemaPersonDetailSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def comments_to_person(request, pk):
    """
    Display comments to person selected by visitor in 'JSON' and 'API' formats.

    Add new comment to cinema person.
    Create "CommentToPerson" model record and save it in DB.

    Only signed-in users will be allowed access to add comment.
    """
    if request.method == 'POST':
        serializer = CommentToPersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        comments = CommentToPerson.objects.filter(
            is_active=True, cinema_person=pk
        )
        serializer = CommentToPersonSerializer(comments, many=True)
        return Response(serializer.data)
