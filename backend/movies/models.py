from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
  genre_id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=50)
  name_kr = models.CharField(max_length=50)

  def __str__(self):
        return self.name
  

class Movie(models.Model):
  tmdb_id = models.IntegerField(primary_key=True)
  title = models.CharField(max_length=255)
  poster_path = models.CharField(max_length=255, null=True, blank=True)
  release_date = models.CharField(null=True, blank=True)
  vote_average =  models.FloatField()
  overview = models.TextField(null=True, blank=True)
  # genres = models.CharField(max_length=255, default='[]') # array of integers
  genres = models.ManyToManyField(Genre, related_name='movies')
  runtime = models.IntegerField(null=True, blank=True) # detail api에서 가져와야 함
  list_type = models.CharField(max_length=50) # 데이터 저장할 때 now_playing, popular 중 저장
  backdrop_paths = models.TextField(null=True, blank=True) # array of backdrop paths

  # 사용자들과의 관계 (M:N)
  like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
  wish_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='wish_movies')
  watched_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='watched_movies')
   
  def __str__(self):
    return self.title


