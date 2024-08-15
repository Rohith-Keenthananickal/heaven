from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
import logging
from PIL import Image
import cv2


class UserDetails(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + str(self.uploaded_at)


logger = logging.getLogger(__name__)

@receiver(post_save, sender=Video)
def generate_thumbnail(sender, instance, **kwargs):
    if instance.video_file and not instance.thumbnail:
        video_path = instance.video_file.path
        thumbnail_directory = os.path.join('media', 'thumbnails')
        os.makedirs(thumbnail_directory, exist_ok=True)  # Ensure the directory exists

        thumbnail_path = os.path.join(thumbnail_directory, f'thumbnail_{instance.id}.png')
        
        try:
            generate_video_thumbnail(video_path, thumbnail_path)
            # Save the relative path to the thumbnail
            instance.thumbnail = thumbnail_path[len('media/'):]
            instance.save()
            logger.info(f'Thumbnail generated and saved for video {instance.id}')
        except Exception as e:
            logger.error(f'Error generating thumbnail for video {instance.id}: {e}')

def generate_video_thumbnail(video_path, thumbnail_path):
    # Open the video file and extract the first frame as a thumbnail
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise Exception(f"Failed to read video frame from {video_path}")

    # Convert the frame from BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Resize the frame to thumbnail size
    thumbnail_size = (300, 300)
    thumbnail = cv2.resize(frame_rgb, thumbnail_size)

    # Save the resized frame as a thumbnail using Pillow
    thumbnail_image = Image.fromarray(thumbnail)
    thumbnail_image.save(thumbnail_path)

# logger = logging.getLogger(__name__)

# @receiver(post_save, sender=Video)
# def generate_thumbnail(sender, instance, **kwargs):
#     if instance.video_file and not instance.thumbnail:
#         video_path = instance.video_file.path
#         thumbnail_path = os.path.join('media', 'thumbnails', f'thumbnail_{instance.id}.png')
#         try:
#             generate_thumbnail(video_path, thumbnail_path)
#             instance.thumbnail = thumbnail_path[len('media/'):]
#             instance.save()
#             logger.info(f'Thumbnail generated and saved for video {instance.id}')
#         except Exception as e:
#             logger.error(f'Error generating thumbnail for video {instance.id}: {e}')

# def generate_thumbnail(video_path, thumbnail_path):
#     # Open the video file and extract the first frame as a thumbnail
#     cap = cv2.VideoCapture(video_path)
#     ret, frame = cap.read()
#     cap.release()

#     # Resize the frame to thumbnail size
#     thumbnail_size = (300, 300)
#     thumbnail = cv2.resize(frame, thumbnail_size)

#     # Save the resized frame as a thumbnail using Pillow
#     thumbnail_image = Image.fromarray(thumbnail)
#     thumbnail_image.save(thumbnail_path)