from django.forms import ModelForm

from .models import Album, Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        exclude = ['user', 'created_on']

class AlbumForm(ModelForm):
    class Meta:
        model = Album
        exclude = ['audioDB_albumID', 'audioDB_artistID', 'score']