from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Event(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  title = models.CharField(max_length=100)
  description = models.CharField(max_length=100)
  upload = models.ImageField(upload_to ='uploads/')
  owner = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
  )
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    # This must return a string
    return f"'{self.title}'\n{self.description}.\n Was created on {self.created_at} by {self.owner}"

  def as_dict(self):
    """Returns dictionary version of timeline models"""
    return {
        'id': self.id,
        'title': self.title,
        'description': self.description,
        'owner': self.owner,
        'created': self.created_at
    }