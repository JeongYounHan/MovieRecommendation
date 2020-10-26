from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class Genre(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return str(self.name)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    release_date = models.DateField(null=True)
    popularity = models.FloatField(null=True)
    vote_count = models.IntegerField(null=True)
    vote_average = models.FloatField(null=True)
    adult = models.BooleanField(null=True)
    overview = models.TextField(null=True)
    original_language = models.CharField(max_length=100, null=True)
    poster_path = models.CharField(max_length = 100)
    backdrop_path = models.CharField(max_length = 100, null=True)
    genres = models.ManyToManyField(Genre, related_name='movie_genres')
    # 기존의 좋아요 기능은 보고싶어요 기능으로 변경
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                    related_name='like_movies')
    def __str__(self):
        return str(self.title)





# 평점 매기는 테이블 하나 생성
class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 최대 10점 작동 안하는듯....확인필요
    ratings = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(10)])
    # 커멘트
    content = models.TextField()