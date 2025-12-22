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
    class Meta:
        model = Movie
        fields = ('tmdb_id', 'poster_path', 'title', 'release_data', 'genre',) # 예고편 추가?

# MovieListSerializer 로컬 버전(?) - 데이터 없어서 검증은 안됨
# class MovieListSerializer(serializers.ModelSerializer):
#     # 외부 URL 대신 로컬 서버의 이미지 주소를 생성
#     local_poster_url = serializers.SerializerMethodField()

#     class Meta:
#         model = Movie
#         fields = ('tmdb_id', 'local_poster_url', 'title', 'vote_average')

#     def get_local_poster_url(self, obj):
#         # 만약 media/posters/ 폴더에 '영화ID.jpg'로 저장되어 있다면
#         if obj.poster_path:
#             # 예: /media/posters/278.jpg
#             return f"/media/posters/{obj.tmdb_id}.jpg"
#         return None
