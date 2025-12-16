from django.db import models
from django.conf import settings
# Create your models here.
class Movie(models.Model):
  movie_id = models.IntegerField()
  genre = models.IntegerField()
  title = models.CharField()
  poster = models.CharField()
  release_date = models.CharField()

class Genre(models.Model):
  name = models.CharField()
  genre_id = models.IntegerField()
  movie_id = models.ForeignKey()
