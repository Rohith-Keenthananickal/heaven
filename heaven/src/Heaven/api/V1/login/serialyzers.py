from rest_framework.serializers import ModelSerializer
from Web.models import UserDetails
from rest_framework import serializers
from Web.models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'video_file', 'thumbnail', 'uploaded_at']

        
class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ('id', 'username', 'password')