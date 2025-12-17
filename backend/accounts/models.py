from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Genre
# Create your models here.

class User(AbstractUser):
  age = models.PositiveIntegerField(null=True, blank=True)
  favorite_genres = models.ManyToManyField(
    'movies.Genre',
    blank=True,
    related_name='users'
  )