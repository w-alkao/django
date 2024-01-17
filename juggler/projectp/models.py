from django.db import models

# Create your models here.

class Project(models.Model):
  name = models.CharField(max_length=50, help_text="The project name.")



class Task(models.Model):
  name = models.CharField(max_length=50, help_text="The task name.")
  project = models.ForeignKey(Project, on_delete=models.CASCADE)