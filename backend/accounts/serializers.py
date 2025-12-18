from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User
from movies.models import Genre, Movie
from reviews.models import Review


# 회원가입
class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    age = serializers.IntegerField(required=True)
    gender = serializers.ChoiceField(
        choices=[('M', '남성'), ('F', '여성')],
        required=True
    )
    favorite_genres = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        allow_empty=False
    )

    def save(self, request):
        user = User(
            username=self.validated_data.get('username'),
            email=self.validated_data.get('email'),
            age=self.validated_data.get('age'),
            gender=self.validated_data.get('gender'),
        )
        user.set_password(self.validated_data.get('password1'))
        user.save()

        genres = Genre.objects.filter(
            genre_id__in=self.validated_data['favorite_genres']
        )
        user.favorite_genres.set(genres)

        return user
    

User = get_user_model()

# 영화 간략 정보용
class MovieSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('tmdb_id', 'title', 'poster_path')


# 리뷰 간략 정보용
class ReviewSimpleSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    class Meta:
        model = Review
        fields = ('id', 'movie_title', 'content', 'rating')


class ProfileSerializer(serializers.ModelSerializer):
    like_movies = MovieSimpleSerializer(many=True, read_only=True)
    wish_movies = MovieSimpleSerializer(many=True, read_only=True)
    watched_movies = MovieSimpleSerializer(many=True, read_only=True)
    reviews = ReviewSimpleSerializer(many=True, read_only=True)
    review_count = serializers.IntegerField(source='reviews.count', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'bio', 'review_count', 'reviews', 'like_movies', 'wish_movies', 'watched_movies')