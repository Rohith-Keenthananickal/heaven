from rest_framework import serializers
from .models import Video
# from rest_framework.pagination import PaginationSerializer

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class PaginatedVideoSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    results = VideoSerializer(many=True)