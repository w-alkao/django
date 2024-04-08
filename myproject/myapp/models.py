from django.db import models

# Create your models here.

class ExampleModel(models.Model):
  image_field = models.ImageField(upload_to="images/")
  file_field = models.FileField(upload_to="files/")
