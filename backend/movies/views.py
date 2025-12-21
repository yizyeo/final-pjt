from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Genre, Movie
from .serializers import (GenreSerializer, 
                          HomeBackdropSerializer, 
                          HomeListSerializer, 
                          MovieDetailSerializer, 
                          MovieListSerializer,)
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField

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
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieDetailSerializer(movie)
    return Response(serializer.data)

@api_view(['POST'])
def movie_like():
    pass

@api_view(['GET'])
def movie_list(request):
    now = timezone.now()
    # 개봉일만 오늘 이전인 영화
    # movies = Movie.objects.filter(release_date__lte=now).order_by('-release_date')[:20]
    # serializer = MovieListSerializer(movies, many=True)
    # return Response(serializer.data)

    # 개봉일 + now_playing 우선
    movies = Movie.objects.filter(release_date__lte=now)

    movies = movies.annotate(
        priority=Case(
            When(list_type='now_playing', then=Value(0)),
            default=Value(1),
            output_field=IntegerField(),
        )
    ).order_by('priority', '-release_date')[:20] # 일단 임시로 20개만

    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

    # 확인 결과 큰 차이 없음 popularity를 가져와서 조건 추가하는게...
    