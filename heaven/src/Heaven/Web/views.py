from django.shortcuts import render,redirect, get_object_or_404

from django.http import HttpResponse
from .models import UserDetails
from .models import Video
from .forms import VideoUploadForm
# import cv2
import cv2
import os

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
    your_view_function(request)
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


def your_view_function(request):
    # Your logic to get the directory path
    video_directory = 'C:\\Users\\LENOVO\\Desktop\\heaven\\src\Heaven\\media\\all_videos'
    


    # Call the upload function
    upload_all_videos_from_directory(video_directory)

    # Continue with the rest of your view logic