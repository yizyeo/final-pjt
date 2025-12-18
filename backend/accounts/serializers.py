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