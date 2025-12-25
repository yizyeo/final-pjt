from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User
from movies.models import Genre, Movie
from reviews.models import Review

User = get_user_model()

# 회원가입
class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    
    age = serializers.IntegerField(min_value=1, max_value=120)
    gender = serializers.ChoiceField(choices=[('M', '남성'), ('F', '여성')])
    favorite_genres = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("이미 존재하는 아이디입니다.")
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("이미 가입된 이메일입니다.")
        return email

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['age'] = self.validated_data.get('age')
        data['gender'] = self.validated_data.get('gender')
        data['favorite_genres'] = self.validated_data.get('favorite_genres')
        return data

    def custom_signup(self, request, user):
        user.age = self.validated_data.get('age')
        user.gender = self.validated_data.get('gender')
        
        genre_ids = self.validated_data.get('favorite_genres')
        if genre_ids:
            genres = Genre.objects.filter(genre_id__in=genre_ids)
            user.favorite_genres.set(genres)
        
        user.save()
    

# 영화 간략 정보
class MovieSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('tmdb_id', 'title', 'poster_path')


# 리뷰 간략 정보
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
        fields = ('id', 'bio', 'email', 'age', 'gender', 'favorite_genres', 'username', 'review_count', 'reviews', 'like_movies', 'wish_movies', 'watched_movies')


# 회원정보 수정
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'age', 'gender', 'favorite_genres')