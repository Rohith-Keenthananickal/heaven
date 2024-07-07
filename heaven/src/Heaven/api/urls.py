# urls.py
from django.urls import path,re_path
from Web.views import VideoListView,getParticularVideo,uploadVideo


urlpatterns = [
    path('videos/search', VideoListView.as_view(), name='video-list'),
    path('video/<int:pk>', getParticularVideo, name='getParticularVideo'),
    path('video/upload', uploadVideo, name='uploadVideo'),
]