from django.db import models
from django.conf import settings
# Create your models here.
class Movie(models.Model):
  # movie_id = models.IntegerField()
  # genre = models.IntegerField()
  # title = models.CharField()
  # poster = models.CharField()
  # release_date = models.CharField()
  tmdb_id = models.IntegerField(primary_key=True)
  title = models.CharField(max_length=255)
  poster_path = models.CharField(max_length=255, null=True, blank=True)
  release_date = models.CharField(null=True, blank=True)
  vote_average =  models.FloatField()
  overview = models.TextField(null=True, blank=True)
  list_type = models.CharField(max_length=50, default='')
  
  def __str__(self):
    return self.title


# class Genre(models.Model):
#   name = models.CharField()
#   genre_id = models.IntegerField()
#   movie_id = models.ForeignKey()
