from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.db.models import Count

from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from movies.models import Movie
import openai
import traceback

# 전체 리뷰 조회
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def total_review_list(request):
    sort = request.GET.get('sort', 'latest')
    
    if sort == 'popular':
        reviews = Review.objects.annotate(
            like_count=Count('like_users')
        ).order_by('-like_count', '-created_at')
    else:
        reviews = Review.objects.order_by('-created_at')
        
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


# 특정 영화의 리뷰 조회 및 작성 (영화 상세 페이지용)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def movie_review_list_or_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    if request.method == 'GET':
        reviews = movie.reviews.order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 리뷰 상세 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def review_detail_update_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    # 본인 확인 로직 (수정/삭제 공통)
    if request.user != review.user:
        return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        review.delete()
        return Response({'message': '리뷰가 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)


# 리뷰 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_like(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if review.like_users.filter(pk=request.user.pk).exists():
        review.like_users.remove(request.user)
        is_liked = False
    else:
        review.like_users.add(request.user)
        is_liked = True
    return Response({'is_liked': is_liked, 'like_count': review.like_users.count()})


# 댓글 작성
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, review=review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# 댓글 삭제
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    if request.user != comment.user:
        return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        
    comment.delete()
    return Response({'message': '댓글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)


# 블라인드 리뷰용 영화 선택
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_blind_review_recommendations(request):
    try:
        user = request.user
        
        # 1. 사용자 정보 가져오기
        try:
            # 장르 필드명 확인 (name_kr 우선 시도, 실패 시 name)
            if hasattr(user, 'favorite_genres'):
                try:
                    favorite_genres = list(user.favorite_genres.values_list('name_kr', flat=True))
                except:
                    favorite_genres = list(user.favorite_genres.values_list('name', flat=True))
            else:
                favorite_genres = []
            
            liked_movies = list(user.like_movies.values_list('title', flat=True)[:10])
            
        except Exception:
            # 에러 발생 시 빈 리스트로 안전하게 처리
            favorite_genres = []
            liked_movies = []

        # 2. OpenAI 클라이언트 설정
        client = openai.OpenAI(
            api_key=settings.OPENAI_API_KEY, 
            base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1"
        )

        # 3. AI 요청
        system_message = "당신은 영화 추천 전문가입니다."
        user_prompt = f"""
        사용자 취향:
        - 선호 장르: {', '.join(favorite_genres) if favorite_genres else '없음'}
        - 좋아하는 영화: {', '.join(liked_movies) if liked_movies else '없음'}
        
        미션:
        1. 이 사용자가 좋아할만한 영화 20개를 추천해줘.
        2. 한국어 제목으로만 쉼표(,)로 구분해서 나열해.
        3. 설명 없이 제목만 출력해.
        """

        recommended_titles = []
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5,
            )
            ai_data = response.choices[0].message.content.strip()
            recommended_titles = [t.strip() for t in ai_data.split(',')]
        except Exception as ai_error:
            print(f">>> [WARN] AI 호출 실패: {ai_error}")
            recommended_titles = []

        # 4. DB 매칭
        final_reviews = []
        
        # 4-1. AI 추천작 검색
        for title in recommended_titles:
            clean_title = title.replace(" ", "")
            movie = Movie.objects.filter(Q(title__icontains=title) | Q(title__icontains=clean_title)).first()
            
            if movie:
                review = Review.objects.filter(movie=movie, is_spoiler=False).first()
                
                # 중복 체크
                is_duplicate = False
                for r in final_reviews:
                    if r['id'] == review.id:
                        is_duplicate = True
                        break
                
                if review and not is_duplicate:
                    final_reviews.append(ReviewSerializer(review).data)
            
            if len(final_reviews) >= 10:
                break
        
        # 4-2. 부족분 채우기 (장르 기반)
        if len(final_reviews) < 10:
            # 장르 기반 영화 검색
            try:
                genre_movies = Movie.objects.filter(genres__name_kr__in=favorite_genres).distinct()
            except:
                genre_movies = Movie.objects.filter(genres__name__in=favorite_genres).distinct()

            # 이미 뽑힌 영화 ID 목록
            existing_ids = [r['movie'] for r in final_reviews]

            needed = 10 - len(final_reviews)
            
            candidates = Review.objects.filter(
                movie__in=genre_movies, 
                is_spoiler=False
            ).exclude(movie__in=existing_ids).order_by('?')[:needed]
            
            for review in candidates:
                final_reviews.append(ReviewSerializer(review).data)
        
        return Response(final_reviews)

    except Exception as e:
        error_msg = traceback.format_exc()
        print("🔥 [서버 에러 상세]:")
        print(error_msg)
        return Response({'error_detail': str(e), 'trace': error_msg}, status=500)