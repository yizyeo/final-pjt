from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Genre, Movie
from .serializers import (GenreSerializer, 
                          HomeBackdropSerializer, 
                          HomeListSerializer, 
                          MovieDetailSerializer, 
                          MovieListSerializer,
                          SearchSerializer,
                          WorldcupSerializer)
import random
from datetime import date
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
def movie_like(request):
    pass

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_wish(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if movie.wish_users.filter(pk=request.user.pk).exists():
        movie.wish_users.remove(request.user)
        is_wished = False
    else:
        movie.wish_users.add(request.user)
        is_wished = True
    return Response({'is_wished': is_wished})

@api_view(['GET'])
def movie_list(request):
    pass


@api_view(['GET'])
def search(request):
    query = request.GET.get('q')
    if query:
        movies = Movie.objects.filter(title__icontains=query)
        serializer = SearchSerializer(movies, many=True)
        return Response(serializer.data)
    return Response([])

@api_view(['GET'])
def random_worldcup(request):
    count = int(request.GET.get('count', 16))
    # 개봉 중이거나 개봉했던 영화 필터링 (release_date가 오늘보다 작거나 같은 경우)
    # release_date가 string이므로 비교를 위해 주의 필요. 포맷이 YYYY-MM-DD라고 가정.
    today = date.today().isoformat()
    movies = Movie.objects.filter(release_date__lte=today, poster_path__isnull=False).exclude(poster_path='')
    
    # 전체 영화 수보다 요청 개수가 많으면 전체 반환
    if movies.count() < count:
        selected_movies = movies
    else:
        # 랜덤 샘플링을 위해 id 리스트를 가져옴 (효율성)
        movie_ids = list(movies.values_list('tmdb_id', flat=True))
        selected_ids = random.sample(movie_ids, count)
        selected_movies = movies.filter(tmdb_id__in=selected_ids)
        
    serializer = WorldcupSerializer(selected_movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_based_worldcup(request):
    # 사용자 선호도 기반 추천 로직 구현 예정 (현재는 틀만 존재)
    # 1. 사용자가 좋아요한 영화, 본 영화, 찜한 영화 가져오기
    # 2. 선호 장르 분석
    # 3. 해당 장르의 영화 중 안 본 영화 추천 등
    
    count = int(request.GET.get('count', 16))
    
    # 임시: 랜덤과 동일하게 동작
    today = date.today().isoformat()
    movies = Movie.objects.filter(release_date__lte=today, poster_path__isnull=False).exclude(poster_path='')
    
    if movies.count() < count:
        selected_movies = movies
    else:
        movie_ids = list(movies.values_list('tmdb_id', flat=True))
        selected_ids = random.sample(movie_ids, count)
        selected_movies = movies.filter(tmdb_id__in=selected_ids)
        
    serializer = WorldcupSerializer(selected_movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def worldcup(request):
    pass
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
    
