from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Web.models import UserDetails
from .serialyzers import CustomUserSerializer
from rest_framework.authtoken.models import Token

import os
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from Web.models import Video
from .serialyzers import VideoSerializer
from Heaven import settings

from drf_yasg.utils import swagger_auto_schema


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if username and password:
            try:
                # Try to get the user based on the provided username and password
                user = UserDetails.objects.get(username=username, password=password)
                return Response({'status': status.HTTP_200_OK,'user_id': user.id}, status=status.HTTP_200_OK)
            except UserDetails.DoesNotExist:
                return Response({'error': 'Invalid credentials','status': status.HTTP_404_NOT_FOUND}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        


class VideoListCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    # permission_classes = [IsAuthenticated]  # Adjust permissions as needed

    @swagger_auto_schema(
        operation_description="Get list of videos",
        responses={200: VideoSerializer(many=True)}
    )

    def post(self, request, format=None):
        q = request.data.get('q', '')
        if q:
            videos = Video.objects.filter(title__icontains=q)
        else:
            videos = Video.objects.all()

        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    
    
    

    def post(self, request, format=None):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

class VideoDetailView(APIView):
    # permission_classes = [IsAuthenticated]  # Adjust permissions as needed

    def get_object(self, pk):
        return Video.objects.filter(id = pk)

    def get(self, request, pk, format=None):
        print(request)
        print(pk)
        video = self.get_object(pk)
        video_file_url = video if video else None

        if video_file_url:
            print(video_file_url)
            serializer = VideoSerializer(video_file_url, many=True)
            return Response(serializer.data)
            # return Response({'video_file_url': video_file_url})
        else:
            return Response({'detail': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        video = self.get_object(pk)
        serializer = VideoSerializer(video, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        video = self.get_object(pk)
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)