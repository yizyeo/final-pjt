from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Genre

@api_view(['GET'])
def genre_list(request):
    genres = Genre.objects.all().order_by('genre_id')
    data = [
        {
            'id': genre.genre_id,
            'name': genre.name,
            'name_kr': genre.name_kr,
        }
        for genre in genres
    ]
    return Response(data)
