from django.db import models
from django.conf import settings
# Create your models here.
class Movie(models.Model):
  tmdb_id = models.IntegerField(primary_key=True)
  title = models.CharField(max_length=255)
  poster_path = models.CharField(max_length=255, null=True, blank=True)
  release_date = models.CharField(null=True, blank=True)
  vote_average =  models.FloatField()
  overview = models.TextField(null=True, blank=True)
  genres = models.CharField(max_length=255, default='[]') # array of integers
  runtime = models.IntegerField(null=True, blank=True) # detail api에서 가져와야 함
  list_type = models.CharField(max_length=50) # 데이터 저장할 때 now_playing, popular 중 저장
  backdrop_paths = models.TextField(null=True, blank=True) # array of backdrop paths
   
  def __str__(self):
    return self.title


class Genre(models.Model):
  genre_id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=50)
  name_kr = models.CharField(max_length=50)

  def __str__(self):
        return self.name


# class MovieImage(models.Model):
#   # movie_id = models.ForeignKey()
#   pass
