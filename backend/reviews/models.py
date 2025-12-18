# from django.db import models
# from django.conf import settings

# # Create your models here.
# class Review(models.Model):
#   user = models.ForeignKey() # 다대일
#   movie_id = models.ForeignKey() # movie랑 다대일 관계
#   movie_title = models.ForeignKey() # 일대일
#   rating = models.DecimalField()
#   content = models.TextField()
#   is_spoiler = models.BooleanField()
#   # like_count = models.IntegerField()
#   created_at = models.DateTimeField(auto_now_add=True)
#   updated_at = models.DateTimeField(auto_now=True)

# class ReviewLike(models.Model):
#   review_id = models.ForeignKey() # 일대일
#   user_id = models.ForeignKey() # 일대일
#   is_like = models.BooleanField()

# class Comments(models.Model):
#   user = models.ForeignKey()
#   comment = models.TextField()
#   created_at = models.DateTimeField(auto_now_add=True)
#   # comment_like = models.BooleanField() 시간 남으면 구현


from django.db import models
from django.conf import settings
from movies.models import Movie

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)