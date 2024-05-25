from django.urls import path
from . import views

app_name = "Web"
urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup, name="signup"),
    path("signup_form", views.signup_form, name="signup_form"),
    path("login", views.login, name="login"),
    path('upload/', views.upload_video, name='upload_video'),
    path('upload_data/', views.upload, name='upload'),
    path('home', views.home, name='home'),
    path('id/<int:video_id>/', views.video_detail, name='video_detail'),
]