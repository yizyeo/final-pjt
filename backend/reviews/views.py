from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count

from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from movies.models import Movie

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
        # 해당 영화의 리뷰만 필터링
        reviews = movie.reviews.order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 리뷰 상세 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def review_detail_update_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    # 조회
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    # 수정
    elif request.method == 'PUT':
        if request.user != review.user:
            return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    # 삭제
    elif request.method == 'DELETE':
        if request.user != review.user:
            return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        
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


# 댓글 생성
def comment_create():
    pass