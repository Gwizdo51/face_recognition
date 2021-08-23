from django.db import models
# from datetime import date
from django.utils.timezone import now


class UploadedImages(models.Model):
    """
    This model saves the images uploaded by the user in MEDIA_ROOT/uploaded_images.
    """
    img_name = models.CharField(max_length=50, default=None, blank=True, null=True)
    uploaded_img = models.ImageField(verbose_name="Select an image to analyze", upload_to='uploaded_images/')
    # analyzed_img_path = models.CharField(max_length=100, default=None, blank=True, null=True)


class ClientDB(models.Model):
    """
    This model is a mock database of known clients and details about them.
    """
    client_name = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField(null=True)
    VIP = models.BooleanField(default=False)
    is_allowed_in = models.BooleanField(default=True)
    comments = models.CharField(max_length=500, default="")
    total_entry_tickets_bought = models.PositiveSmallIntegerField(default=0)
    creation_date = models.DateField(default=now)
