from django.db import models

# Create your models here.

class UploadedImages(models.Model):
    img_name = models.CharField(max_length=50, default=None, blank=True, null=True)
    uploaded_img = models.ImageField(verbose_name="Select an image to analyze", upload_to='uploaded_images/')
    # analyzed_img = models.ImageField(upload_to='analyzed_images/', default=None, null=True)