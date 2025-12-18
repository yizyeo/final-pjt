from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Genre
# Create your models here.

class User(AbstractUser):
  GENDER_CHOICES = (
        ('M', '남성'),
        ('F', '여성'),
    )
  
  age = models.PositiveIntegerField()
  gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES
    )
  favorite_genres = models.ManyToManyField(
    'movies.Genre',
    # blank=True,
    related_name='users'
  )