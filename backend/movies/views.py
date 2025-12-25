from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
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
import requests
from django.conf import settings
from datetime import date
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField
import openai
import re


@api_view(['GET'])
def genre_list(request):
    genres = Genre.objects.all().order_by('genre_id')
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def carousel_backdrop(request):
    popularity_threshold = 25.0
    
    movies = Movie.objects.exclude(backdrop_paths=[]) \
                .filter(
                    release_date__lt='2025-01-01', 
                    popularity__gte=popularity_threshold
                ) \
                .order_by('?')[:10]  # 랜덤하게 섞은 후 상위 10개만 추출
    
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
    serializer = MovieDetailSerializer(movie, context={'request': request})
    data = serializer.data

    # TMDB Credits API 호출 로직 추가
    try:
        api_key = settings.TMDB_API_KEY
        url = f"https://api.themoviedb.org/3/movie/{movie.tmdb_id}/credits"
        params = {
            'api_key': api_key,
            'language': 'ko-KR'
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            credits_data = response.json()
            
            # 1. 감독 찾기 (job이 'Director'인 사람)
            directors = [
                person['name'] 
                for person in credits_data.get('crew', []) 
                if person.get('job') == 'Director'
            ]
            
            # 2. 출연진 찾기 (known_for_department가 'Acting'인 사람)
            # popularity 내림차순 정렬 후 상위 3명
            actors = [
                person 
                for person in credits_data.get('cast', []) 
                if person.get('known_for_department') == 'Acting'
            ]
            actors.sort(key=lambda x: x.get('popularity', 0), reverse=True)
            top_actors = [actor['name'] for actor in actors[:3]]
            
            # 데이터에 추가
            data['credits'] = {
                'directors': directors,
                'actors': top_actors
            }
        else:
            print(f"TMDB API Error: {response.status_code}")
            data['credits'] = {'directors': [], 'actors': []}

    except Exception as e:
        print(f"Credit Fetch Error: {e}")
        data['credits'] = {'directors': [], 'actors': []}

    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if movie.like_users.filter(pk=request.user.pk).exists():
        movie.like_users.remove(request.user)
        is_liked = False
    else:
        movie.like_users.add(request.user)
        is_liked = True
    return Response({'is_liked': is_liked})


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_watched(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if movie.watched_users.filter(pk=request.user.pk).exists():
        movie.watched_users.remove(request.user)
        is_watched = False
    else:
        movie.watched_users.add(request.user)
        is_watched = True
    return Response({'is_watched': is_watched})


@api_view(['GET'])
def movie_list(request):
    now = timezone.now()
    genre_id = request.GET.get('genre')
    year = request.GET.get('year')
    page = int(request.GET.get('page', 1))

    # 기본 필터: 개봉일이 오늘 이전인 영화
    movies = Movie.objects.filter(release_date__lte=now, poster_path__isnull=False
                                  ).exclude(poster_path='')

    # 장르 및 연도 필터링
    if genre_id or year:
        if genre_id:
            movies = movies.filter(genres__genre_id=genre_id)
        if year:
            movies = movies.filter(release_date__startswith=str(year))
        
        movies = movies.order_by('-release_date')[:50] # 필터 적용 시 50개 제한
        
    else:
        # 필터가 없는 경우 기존 로직 (개봉일 + now_playing 우선) + 페이지네이션
        page_size = 20
        offset = (page - 1) * page_size
        
        movies = movies.annotate(
            priority=Case(
                When(list_type='now_playing', then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        ).order_by('priority', '-release_date')[offset : offset + page_size]

    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

    # 확인 결과 큰 차이 없음 popularity를 가져와서 조건 추가하는게...
    

@api_view(['GET'])
def search(request):
    query = request.GET.get('q')
    if query:
        # 띄어쓰기로 분리해서 각 단어가 모두 포함된 영화 검색
        words = query.split()
        
        movies = Movie.objects.filter(
            poster_path__isnull=False
        ).exclude(poster_path='')
        
        # 각 단어가 title에 포함되어야 함
        for word in words:
            movies = movies.filter(title__icontains=word)
        
        # popularity 순으로 정렬
        movies = movies.order_by('-popularity')[:20]
        
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
    count = int(request.GET.get('count', 16))
    user = request.user

    # 1. 사용자 선호 정보 수집
    favorite_genres = ", ".join([g.name_kr for g in user.favorite_genres.all()])
    liked_movies = ", ".join([m.title for m in user.like_movies.all()[:5]])
    wished_movies = ", ".join([m.title for m in user.wish_movies.all()[:5]])
    watched_movies = ", ".join([m.title for m in user.watched_movies.all()[:5]])
    
    # 데이터가 아예 없으면 랜덤으로 처리
    if not (favorite_genres or liked_movies or wished_movies or watched_movies):
        return random_worldcup(request)

    # 2. OpenAI API 호출 준비
    client = openai.OpenAI(
        api_key=settings.OPENAI_API_KEY, 
        base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1"
    )

    system_message = "당신은 사용자의 영화 취향을 완벽하게 파악하는 영화 큐레이터입니다."
    # DB 매칭 실패를 고려해 요청 개수의 3배수 추천 요청
    request_count = count * 3
    
    user_prompt = f"""
    이 사용자의 취향에 맞춰서 영화 이상형 월드컵에 쓸 영화 후보 {request_count}개를 추천해줘.
    
    [사용자 취향 데이터]
    - 선호 장르: {favorite_genres}
    - 좋아요 한 영화: {liked_movies}
    - 찜한 영화: {wished_movies}
    - 봤어요 표시한 영화: {watched_movies}
    
    [요청 사항]
    1. 사용자의 취향과 유사한 결을 가진 영화들을 우선 추천하되, 다양한 장르를 적절히 섞어줘.
    2. 너무 뻔한 영화보다는 작품성이 있거나 숨겨진 명작도 포함해줘.
    3. 결과는 반드시 영화의 '한국어 제목'만 쉼표(,)로 구분해서 한 줄로 나열해줘.
    4. 번호, 설명, 따옴표 등 잡다한 텍스트는 절대 넣지 마.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        ai_response = response.choices[0].message.content.strip()
        recommended_titles = [t.strip() for t in ai_response.split(',')]
        
        # 3. DB에서 영화 찾기
        selected_movies = []
        seen_ids = set()
        
        # 오늘 날짜 기준 (개봉 예정작 제외)
        today = date.today().isoformat()

        for title in recommended_titles:
            if len(selected_movies) >= count:
                break
                
            # 정확한 매칭 시도
            movie = Movie.objects.filter(
                title=title, 
                poster_path__isnull=False,
                release_date__lte=today
            ).exclude(poster_path='').first()
            
            # 유사 매칭 시도 (특수문자/공백 제거)
            if not movie:
                clean_title = re.sub(r'[^가-힣a-zA-Z0-9]', '', title)
                if clean_title:
                    movie = Movie.objects.filter(
                        title__icontains=clean_title,
                        poster_path__isnull=False,
                        release_date__lte=today
                    ).exclude(poster_path='').first()
            
            if movie and movie.tmdb_id not in seen_ids:
                selected_movies.append(movie)
                seen_ids.add(movie.tmdb_id)
        
        # 4. 개수가 부족하면 인기 영화로 채우기
        if len(selected_movies) < count:
            needed = count - len(selected_movies)
            popular_movies = Movie.objects.filter(
                release_date__lte=today,
                poster_path__isnull=False
            ).exclude(poster_path='').order_by('-popularity')[:needed+20] # 넉넉히 가져옴
            
            for movie in popular_movies:
                if len(selected_movies) >= count:
                    break
                if movie.tmdb_id not in seen_ids:
                    selected_movies.append(movie)
                    seen_ids.add(movie.tmdb_id)
        
        # 랜덤하게 섞어서 반환
        random.shuffle(selected_movies)
        
        serializer = WorldcupSerializer(selected_movies, many=True)
        return Response(serializer.data)

    except Exception as e:
        print(f"AI Worldcup Error: {e}")
        # 에러 발생 시 랜덤 월드컵으로 대체
        return random_worldcup(request)


@api_view(['GET'])
@permission_classes([AllowAny])
def movie_trailer(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    tmdb_id = movie.tmdb_id
    api_key = settings.TMDB_API_KEY 
    
    # 1. TMDB API로 비디오 정보 요청
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/videos"
    params = {
        'api_key': api_key,
        'language': 'ko-KR' # 한국어 예고편 우선
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        results = data.get('results', [])
        
        # 2. 한국어 예고편이 없으면 영어로 재시도 (선택 사항)
        if not results:
            params['language'] = 'en-US'
            response = requests.get(url, params=params)
            data = response.json()
            results = data.get('results', [])

        # 3. 결과 중에서 'YouTube'이면서 'Trailer'인 것 찾기
        video_id = None
        
        # 우선순위: Trailer > Teaser
        for video in results:
            if video['site'] == 'YouTube' and video['type'] == 'Trailer':
                video_id = video['key']
                break
        
        # Trailer가 없으면 Teaser라도 가져오기
        if not video_id and results:
             for video in results:
                if video['site'] == 'YouTube':
                    video_id = video['key']
                    break

        if video_id:
            return Response({'videoId': video_id})
        else:
            return Response({'videoId': None, 'message': '예고편을 찾을 수 없습니다.'})

    except Exception as e:
        print(f"Trailer Fetch Error: {e}")
        return Response({'error': '서버 에러가 발생했습니다.'}, status=500)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recommend_by_keyword(request):
    user_input = request.data.get('content')
    
    if not user_input:
        return Response({'message': '추천받고 싶은 상황이나 기분을 입력해주세요.'}, status=400)

    client = openai.OpenAI(
        api_key=settings.OPENAI_API_KEY, 
        base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1"
    )

    system_message = "당신은 사용자의 기분과 상황에 맞춰 대중적으로 잘 알려진 영화를 골라주는 영화 추천 큐레이터입니다."
    user_prompt = f"""
        사용자 요청: "{user_input}"
        
        아래 조건을 모두 만족하는 영화를 추천하세요.

        [추천 기준]
        - 사용자의 요청에서 드러난 감정, 분위기, 상황을 우선 반영
        - 너무 마이너하거나 예술영화 성향의 작품은 제외
        - 특정 시리즈가 있다면 대표작 위주로 선정

        [출력 규칙]
        1. 정확히 20개의 영화 제목만 출력
        2. 반드시 한국어 제목만 사용
        3. 쉼표(,)로만 구분하여 한 줄로 출력
        4. 번호, 설명, 줄바꿈, 따옴표, 이모지, 추가 문구 절대 금지
        5. 결과에는 영화 제목 외 어떤 텍스트도 포함하지 말 것
        """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,
            max_tokens=200
        )
        
        ai_response = response.choices[0].message.content.strip()
        recommended_titles = [t.strip() for t in ai_response.split(',')]
        
        valid_movies = []
        for title in recommended_titles:
            # [검색 전략] 1. 정확히 일치 시도
            movie = Movie.objects.filter(title=title).first()
            
            # 2. 정확히 일치하는 게 없다면 띄어쓰기 제거 후 검색 시도
            if not movie:
                # 제목에서 한글/영문/숫자만 남기고 공백 제거 (예: '스파이더맨 노 웨이 홈' -> '스파이더맨노웨이홈')
                clean_title = re.sub(r'[^가-힣a-zA-Z0-9]', '', title)
                if clean_title:
                    movie = Movie.objects.filter(title__icontains=clean_title).first()

            if movie:
                # 중복 방지 및 최대 10개 제한
                if movie.tmdb_id not in [m['tmdb_id'] for m in valid_movies]:
                    serializer = MovieListSerializer(movie)
                    valid_movies.append(serializer.data)

            if len(valid_movies) >= 8:
                break

        # 4. 결과가 부족할 경우 Fallback (인기 영화 5개 채우기)
        if len(valid_movies) < 5:
            popular_movies = Movie.objects.order_by('-vote_count')[:10]
            for m in popular_movies:
                if len(valid_movies) >= 10: break
                if m.tmdb_id not in [x['tmdb_id'] for x in valid_movies]:
                    valid_movies.append(MovieListSerializer(m).data)

        return Response(valid_movies)

    except Exception as e:
        print(f"GMS OpenAI Error: {e}")
        return Response({'error': '영화 추천 중 오류가 발생했습니다.'}, status=500)


@api_view(['GET'])
def hot_movies(request):
    """now_playing 중 popularity 상위 10개"""
    movies = Movie.objects.filter(
        list_type='popular'
    ).order_by('-popularity')[:10]
    
    serializer = HomeListSerializer(movies, many=True)
    return Response(serializer.data)