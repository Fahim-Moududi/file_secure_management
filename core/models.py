from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class FileUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    encrypted_file = models.FileField(upload_to='encrypted/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size = models.BigIntegerField()
