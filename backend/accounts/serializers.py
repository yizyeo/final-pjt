from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User
from movies.models import Genre, Movie
from reviews.models import Review

User = get_user_model()

# 회원가입
class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': '이메일은 필수 입력 항목입니다.',
            'invalid': '유효한 이메일 형식이 아닙니다.',
        }
    )
    age = serializers.IntegerField(
        required=True,
        min_value=1,
        max_value=120,
        error_messages={
            'required': '나이를 입력해주세요.',
            'min_value': '나이는 1세 이상이어야 합니다.',
            'invalid': '숫자만 입력 가능합니다.'
        }
    )
    gender = serializers.ChoiceField(
        choices=[('M', '남성'), ('F', '여성')],
        required=True,
        error_messages={
            'required': '성별을 선택해주세요.',
            'invalid_choice': '남성 또는 여성 중에서 선택해주세요.'
        }
    )
    favorite_genres = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        allow_empty=False,
        error_messages={
            'required': '최소 하나 이상의 선호 장르를 선택해야 합니다.',
            'empty': '선호 장르를 선택해주세요.'
        }
    )

    # 1. 아이디 중복 체크 커스텀
    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("이미 존재하는 아이디입니다.")
        return username

    # 2. 이메일 중복 체크 커스텀
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("이미 가입된 이메일입니다.")
        return email

    def save(self, request):
        # 부모 클래스의 save 로직을 활용하면서 필요한 필드 추가
        user = super().save(request)
        
        # 추가 필드 저장 (super().save()가 반환한 user 객체 업데이트)
        user.age = self.validated_data.get('age')
        user.gender = self.validated_data.get('gender')
        user.save()

        # 장르 M:N 관계 저장
        genre_ids = self.validated_data.get('favorite_genres')
        if genre_ids:
            genres = Genre.objects.filter(genre_id__in=genre_ids)
            user.favorite_genres.set(genres)

        return user
    

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