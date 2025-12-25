from rest_framework import serializers
from .models import Genre, Movie
import json

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('genre_id', 'name', 'name_kr')
        

class MovieDetailSerializer(serializers.ModelSerializer):
    # DB에는 없지만, 프론트엔드를 위해 계산해서 만들어주는 필드들
    is_liked = serializers.SerializerMethodField()
    is_wished = serializers.SerializerMethodField()
    is_watched = serializers.SerializerMethodField()

    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'

    # 좋아요
    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.like_users.filter(pk=user.pk).exists()
        return False

    # 볼 영화
    def get_is_wished(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.wish_users.filter(pk=user.pk).exists()
        return False

    # 본 영화
    def get_is_watched(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.watched_users.filter(pk=user.pk).exists()
        return False
    

class HomeBackdropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('tmdb_id', 'backdrop_paths', 'title', 'vote_average', 'genres', 'release_date', )


class HomeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('tmdb_id', 'poster_path', 'title', 'vote_average', 'genres',)


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('tmdb_id', 'poster_path', 'title', 'release_date', 'genres', 'vote_average', )


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('tmdb_id', 'poster_path', 'title', 'vote_average',)
        
        
class WorldcupSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ('tmdb_id', 'poster_path', 'title', 'release_date', 'genres',) # 예고편 추가?
