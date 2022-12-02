from django.db import models
from django.contrib.auth import get_user_model
from .event import Event

# Create your models here.
class Timeline(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=100)
  description = models.CharField(max_length=100)
  guest_can_post = models.BooleanField(null=False, default=False)
  owner = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
  )
  events=models.ManyToManyField('Event', related_name='events')

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
