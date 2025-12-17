from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import Genre, User

class CustomRegisterSerializer(RegisterSerializer):
    age = serializers.IntegerField(required=False)
    favorite_genres = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )

    def save(self, request):
        user = super().save(request)

        # age 저장
        user.age = self.validated_data.get('age')
        user.save()

        # 선호 장르 저장
        genre_ids = self.validated_data.get('favorite_genres', [])
        print(f'수신된 장르 ID 목록: {genre_ids}') # 터미널에서 확인용
        if genre_ids:
            genres = Genre.objects.filter(genre_id__in=genre_ids)
            print(f'조회된 장르 객체들: {genres}') # 필터링이 잘 되었는지 확인
            user.favorite_genres.set(genres)

        return user
