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
import random

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
        TARGET_COUNT = 6
        final_reviews = []
        
        # 1-1. 내가 본 영화 (리뷰 쓴 영화) ID 수집
        watched_movie_ids = list(Review.objects.filter(user=user).values_list('movie', flat=True))
        seen_movie_ids = set(watched_movie_ids) # 중복 방지 Set

        # ---------------------------------------------------------
        # 1단계: AI 기반 추천 (가장 높은 우선순위)
        # ---------------------------------------------------------
        try:
            # --- (취향 분석 로직 생략 없이 그대로 사용) ---
            if hasattr(user, 'favorite_genres'):
                try:
                    favorite_genres = list(user.favorite_genres.values_list('name_kr', flat=True))
                except:
                    favorite_genres = list(user.favorite_genres.values_list('name', flat=True))
            else:
                favorite_genres = []

            liked_titles = list(user.like_movies.values_list('title', flat=True)[:5])
            high_rated_titles = list(Review.objects.filter(user=user, rating__gte=7).values_list('movie__title', flat=True)[:5])
            positive_movies = list(set(liked_titles + high_rated_titles))

            client = openai.OpenAI(
                api_key=settings.OPENAI_API_KEY, 
                base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1"
            )
            
            # AI에게 더 많은 후보를 요청 (20개) -> 매칭 확률 높이기
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "영화 추천 전문가입니다."},
                    {"role": "user", "content": f"선호장르: {','.join(favorite_genres)}, 좋아하는영화: {','.join(positive_movies)}. 이 사용자가 좋아할 한국어 영화 제목 20개 추천. 설명 없이 쉼표로 구분."}
                ],
                temperature=0.7,
            )
            ai_titles = [t.strip() for t in response.choices[0].message.content.strip().split(',')]
            
            for title in ai_titles:
                if len(final_reviews) >= TARGET_COUNT: break
                clean_title = title.replace(" ", "")
                movie = Movie.objects.filter(Q(title__icontains=title) | Q(title__icontains=clean_title)).first()

                if movie and (movie.pk not in seen_movie_ids):
                    review = Review.objects.filter(movie=movie, is_spoiler=False).exclude(user=user).order_by('?').first()
                    if review:
                        final_reviews.append(ReviewSerializer(review).data)
                        seen_movie_ids.add(movie.pk)

        except Exception as e:
            print(f">>> 1단계 AI 추천 건너뜀: {e}")
            # AI 에러나도 죽지 않고 2단계로 넘어감

        # ---------------------------------------------------------
        # 2단계: 선호 장르 기반 보충 (중간 우선순위)
        # ---------------------------------------------------------
        if len(final_reviews) < TARGET_COUNT and favorite_genres:
            needed = TARGET_COUNT - len(final_reviews)
            try:
                genre_q = Q(genres__name_kr__in=favorite_genres)
            except:
                genre_q = Q(genres__name__in=favorite_genres)
            
            # 장르 영화 중 안 본 것의 ID 추출
            candidate_movie_ids = list(Movie.objects.filter(genre_q)
                                       .exclude(pk__in=seen_movie_ids)
                                       .values_list('pk', flat=True))
            
            if candidate_movie_ids:
                random.shuffle(candidate_movie_ids)
                for movie_id in candidate_movie_ids:
                    if len(final_reviews) >= TARGET_COUNT: break
                    
                    review = Review.objects.filter(movie_id=movie_id, is_spoiler=False)\
                                           .exclude(user=user).order_by('?').first()
                    if review:
                        final_reviews.append(ReviewSerializer(review).data)
                        seen_movie_ids.add(movie_id)

        # ---------------------------------------------------------
        # [NEW] 3단계: 긴급 보충 (Safety Net - 최후의 수단)
        # ---------------------------------------------------------
        # 아직도 6개가 안 찼다면? 장르 상관없이 DB에 있는 '유효한 리뷰' 아무거나 가져옴
        if len(final_reviews) < TARGET_COUNT:
            needed = TARGET_COUNT - len(final_reviews)
            print(f">>> [System] 3단계 진입: 부족한 {needed}개를 전체 리뷰에서 채웁니다.")

            # 조건: 스포일러X, 내꺼X, 이미 뽑은 영화X
            # 정렬: 최신순(-created_at) 혹은 랜덤('?') -> 랜덤 추천
            backup_reviews = Review.objects.filter(is_spoiler=False)\
                                           .exclude(user=user)\
                                           .exclude(movie__pk__in=seen_movie_ids)\
                                           .order_by('?')[:needed]
            
            for review in backup_reviews:
                final_reviews.append(ReviewSerializer(review).data)

        return Response(final_reviews)

    except Exception as e:
        error_msg = traceback.format_exc()
        print("🔥 [Critical Error]:", error_msg)
        return Response({'error': 'Internal Error', 'detail': str(e)}, status=500)