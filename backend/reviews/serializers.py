from rest_framework import serializers
from .models import Review, Comment


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'username', 'content', 'created_at', 'updated_at')
        read_only_fields = ('review', 'user')


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    movie_poster = serializers.CharField(source='movie.poster_path', read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = (
            'id', 'username', 'movie', 'movie_title', 'movie_poster', 
            'content', 'rating', 'created_at', 'updated_at', 
            'like_count', 'comments'
        )
        read_only_fields = ('user',)