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
        thumbnail_path = os.path.join('media', 'thumbnails', f'thumbnail_{instance.id}.png')
        try:
            generate_thumbnail(video_path, thumbnail_path)
            instance.thumbnail = thumbnail_path[len('media/'):]
            instance.save()
            logger.info(f'Thumbnail generated and saved for video {instance.id}')
        except Exception as e:
            logger.error(f'Error generating thumbnail for video {instance.id}: {e}')

def generate_thumbnail(video_path, thumbnail_path):
    # Open the video file and extract the first frame as a thumbnail
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()

    # Resize the frame to thumbnail size
    thumbnail_size = (300, 300)
    thumbnail = cv2.resize(frame, thumbnail_size)

    # Save the resized frame as a thumbnail using Pillow
    thumbnail_image = Image.fromarray(thumbnail)
    thumbnail_image.save(thumbnail_path)