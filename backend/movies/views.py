from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Genre
from .serializers import GenreSerializer

@api_view(['GET'])
def genre_list(request):
    genres = Genre.objects.all().order_by('genre_id')
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)
