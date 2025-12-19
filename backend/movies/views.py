from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Genre, Movie
from .serializers import GenreSerializer, HomeBackdropSerializer, HomeListSerializer

@api_view(['GET'])
def genre_list(request):
    genres = Genre.objects.all().order_by('genre_id')
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def carousel_backdrop(request):
    movies = Movie.objects.all() # 이렇게 하면 되는지 확인
    serializer = HomeBackdropSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def home_list(request):
    movies = Movie.objects.all() # 이렇게 하면 되는지 확인
    serializer = HomeListSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_detail(request):
    pass

@api_view(['POST'])
def movie_like():
    pass