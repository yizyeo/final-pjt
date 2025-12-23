from rest_framework import serializers
from .models import Genre, Movie
import json

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('genre_id', 'name', 'name_kr')
        
class MovieDetailSerializer(serializers.ModelSerializer):
    # backdrop_paths = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'
    
    # def get_backdrop_paths(self, obj):
    #     if isinstance(obj.backdrop_path, str):
    #         try:
    #             return json.loads(obj.backdrop_path.replace("'", '"'))
    #         except:
    #             return []
    #     return obj.backdrop_path

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
        fields = ('tmdb_id', 'poster_path', 'title', 'release_date', 'genres', )


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('tmdb_id', 'poster_path', 'title', 'vote_average',)
        
        
class WorldcupSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ('tmdb_id', 'poster_path', 'title', 'release_date', 'genres',) # 예고편 추가?
