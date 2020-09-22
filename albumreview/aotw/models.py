from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    pass

class Album(models.Model):
    idAlbum = models.PositiveIntegerField(blank=True, unique=True)
    strAlbum = models.CharField(max_length=200)
    strDescriptionEN = models.TextField(blank=True)
    strArtist = models.CharField(max_length=100)
    idArtist = models.PositiveIntegerField(blank=True, null=True)
    strAlbumThumb = models.URLField(blank=True)
    intYearReleased = models.PositiveSmallIntegerField(blank=True)
    strLabel = models.CharField(max_length=100, blank=True)
    strGenre = models.CharField(max_length=100, blank=True)
    score = models.SmallIntegerField(blank=True, null=True)
    custom = models.BooleanField(default=False)

    def __str__(self):
        return(f'{self.strAlbum} by {self.strArtist}')
    
class Nomination(models.Model):
    album = models.OneToOneField(Album, on_delete=models.CASCADE)
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
            self.aotw_date = timezone.now()
        super(Nomination, self).save(*args, **kwargs)

    def __str__(self):
        return(f'{self.album.strAlbum} nominated by {self.user}')

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

