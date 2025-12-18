from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import Genre, User

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
        user = super().save(request)

        user.age = self.validated_data['age']
        user.gender = self.validated_data['gender']
        user.save()

        genre_ids = self.validated_data['favorite_genres']
        genres = Genre.objects.filter(genre_id__in=genre_ids)
        user.favorite_genres.set(genres)

        return user