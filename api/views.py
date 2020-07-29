from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from cinema.models import Film, CommentToFilm, News, CommentToNews
from .serializers import FilmListSerializer, FilmDetailSerializer, \
    CommentToFilmSerializer, NewsListSerializer, NewsDetailSerializer, \
    CommentToNewsSerializer


class FilmListView(ListAPIView):
    queryset = Film.objects.order_by('pk')
    serializer_class = FilmListSerializer


class FilmDetailView(RetrieveAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmDetailSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def comments_to_film(request, pk):
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
    queryset = News.objects.order_by('pk')
    serializer_class = NewsListSerializer


class NewsDetailView(RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsDetailSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def comments_to_news(request, pk):
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
