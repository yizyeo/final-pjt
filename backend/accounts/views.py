from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ProfileSerializer, UserUpdateSerializer

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_detail(request, username):
    person = get_object_or_404(User, username=username)
    serializer = ProfileSerializer(person)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_update(request):
    user = request.user
    serializer = UserUpdateSerializer(user, data=request.data, partial=True)
    
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)