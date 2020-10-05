from django.forms import ModelForm
from django.core.files.images import get_image_dimensions

from .models import Album, Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        exclude = ['user', 'created_on']
        

class AlbumForm(ModelForm):
    class Meta:
        model = Album
        exclude = ['idAlbum', 'idArtist', 'score', 'custom']

