from django.shortcuts import render,redirect, get_object_or_404

from django.http import HttpResponse

from api.V1.login.serialyzers import VideoSerializer
from .serializers import PaginatedVideoSerializer
from .models import UserDetails
from .models import Video
from .forms import VideoUploadForm
# import cv2
import cv2
import os

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.csrf import csrf_exempt
from .pagination import VideoPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions, viewsets
from rest_framework.views import APIView

def index(request):
    return render(request, 'login/login.html')


def signup(request):
    return render(request, 'signup/signup.html')

def signup_form(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    if username and password:
        return HttpResponse("success")
    else:
        return HttpResponse("failed")
    
def login(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    print(username,password)
    print(UserDetails.password)
    if UserDetails.objects.get(username=username) and UserDetails.objects.get(password=password):
        
        return redirect('/home')
    else:
        return HttpResponse("failed to login")
    

def home(request):
    # your_view_function(request)
    videos= Video.objects.all()
    context={
        "videos": videos
    }
    print(context)
    return render(request, 'listing_page/home.html', context=context)


def upload(request):
    return render(request, 'upload/upload.html')


def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)

            # Save the video file
            video.video_file = form.cleaned_data['video_file']
            video.save()

            # No need to generate and save the thumbnail here, as it's handled by the post_save signal

            return redirect('listing_page/home.html')  # Redirect to the video list page or any other page after successful upload
    else:
        form = VideoUploadForm()
    
    return render(request,'upload/upload.html', {'form': form})


def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    
    return render(request, 'listing_page/view.html', {'video': video, 'video_name': video.title})



def upload_video_function(title, file_path):
    video = Video(title=title, video_file=file_path)
    video.save()


def upload_all_videos_from_directory(directory_path):
    video_files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    
    for video_file in video_files:
        chechIfExists=Video.objects.filter(title=video_file.title).exists()
        if chechIfExists:
            print("updated")
        else:
            title = os.path.splitext(os.path.basename(video_file))[0]  # Use the file name as the title (without extension)
            file_path = os.path.join(directory_path, video_file)
            upload_video_function(title, file_path)


# def your_view_function(request):
#     # Your logic to get the directory path
#     video_directory = 'C:\\Users\\LENOVO\\Desktop\\heaven\\src\Heaven\\media\\all_videos'
    


#     # Call the upload function
#     upload_all_videos_from_directory(video_directory)

#     # Continue with the rest of your view logic


# @api_view(['POST'])
# def listVideos(request):
#     if request.method == 'POST':
#         q = request.data.get('q')
#         page_number = request.data.get('page', 1)  # Default to page 1 if not provided

#         if q:
#             videos = Video.objects.filter(title__icontains=q).order_by('id')
#         else:
#             videos = Video.objects.all().order_by('id')

#         paginator = PageNumberPagination()
#         paginator.page_size = 10  # Adjust page size as needed
#         paginated_videos = paginator.paginate_queryset(videos, request)

#         serializer = VideoSerializer(paginated_videos, many=True)
#         custom_data = {
#             'totalRecords': paginator.page.paginator.count,
#             'totalPages': paginator.page.paginator.num_pages,
#             'currentPage': page_number,  # Use the provided page_number
#             'next': paginator.get_next_link(),
#             'previous': paginator.get_previous_link(),
#             'results': serializer.data , # Serialize the paginated data
#             'recordsPerPage': len(serializer.data),  # Number of records in the current page
#         }

#         return Response(custom_data)


class VideoListView(APIView):
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        videos = Video.objects.all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(videos, request)
        if page is not None:
            serializer = VideoSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

# @api_view(['POST'])
# def listVideos(request):
#     q = request.query_params.get('q')
#     if q:
#         videos = Video.objects.filter(title__icontains=q).order_by('id')
#     else:
#         videos = Video.objects.all().order_by('id')
        
#     serializer = VideoSerializer(videos, many=True)
#     return Response(serializer.data)  # Use serializer.data, not just serializer


@api_view(['GET'])
def getParticularVideo(request, pk):
    video = get_object_or_404(Video, pk=pk)
    serializer = VideoSerializer(video)
    return Response(serializer.data)


@api_view(['POST'])
def uploadVideo(request):
    if request.method == 'POST':
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)