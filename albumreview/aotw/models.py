from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    pass

class Album(models.Model):
    audioDB_albumID = models.PositiveIntegerField(blank=True, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    artist = models.CharField(max_length=100)
    audioDB_artistID = models.PositiveIntegerField(blank=True, unique=True)
    album_art = models.URLField(blank=True)
    year = models.PositiveSmallIntegerField(blank=True)
    label = models.CharField(max_length=100, blank=True)
    genre = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return(f'{self.title} by {self.artist}')
    
class Nomination(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    created_on = models.DateTimeField(auto_now_add=True)

    aotw = models.BooleanField(default=False)
    aotw_date = models.DateField('date as AOTW', null=True, blank=True)
    active = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(Nomination, self).__init__(*args, **kwargs)
        self._aotw = self.aotw

    def save(self, *args, **kwargs):
        if not self._aotw and self.aotw:
            self.aotw_date = django.timezone.now()
        super(Nomination, self).save(*args, **kwargs)

    def __str__(self):
        return(f'{self.album.title} nominated by {self.user}')

class Review(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    created_on = models.DateTimeField(auto_now_add=True)
    review_text = models.TextField(blank=True)
    top_tracks = models.TextField(blank=True)
    rating = models.SmallIntegerField(default=0, validators=[
            MaxValueValidator(5),
            MinValueValidator(-5)
        ])
    

