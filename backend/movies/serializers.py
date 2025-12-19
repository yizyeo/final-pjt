from rest_framework import serializers
from .models import Genre, Movie

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('genre_id', 'name', 'name_kr')
        
class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class HomeBackdropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('tmdb_id', 'backdrop_paths', 'title', 'vote_average', 'genres', 'release_date', )

class HomeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('tmdb_id', 'poster_path', 'title', 'vote_average', 'genres',)
        
class MovieSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('tmdb_id', 'poster_path', 'title', 'release_date', 'genres', )
        