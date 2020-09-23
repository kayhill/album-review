from .models import User, Album, Nomination, Review
from titlecase import titlecase

import requests 

def addalbum(album):
    album.strAlbum = titlecase(album.strAlbum)
    album.strArtist = titlecase(album.strArtist)
    album.strGenre = titlecase(album.strGenre)
    album.strLabel = titlecase(album.strLabel)
    customalbs = Album.objects.filter(custom=True)   
    i = len(customalbs) + 1
    randomID = 999900000 + i
    album.idAlbum = randomID
    album.custom = True
    album.save()

def nominate(user, album_id):
    ## check if album in db
    try:
        checkalb = Album.objects.get(idAlbum=album_id)

        try:
            nom = Nomination.objects.get(album=checkalb)
        
        #  add nomination
        except Nomination.DoesNotExist:        
            nom = Nomination()
            nom.album = checkalb
            nom.user = user
            nom.save()           
                

    ## if album not in db:
    except Album.DoesNotExist: 
        # get album info
        response = requests.get('https://theaudiodb.com/api/v1/json/1/album.php?m=%s' % album_id)
        response = response.json()
        album = response['album']
        
        # save to DB 
        for a in album:
            newalb = Album()
            newalb.idAlbum = album_id
            newalb.strAlbum = a['strAlbum']
            try:
                newalb.strDescriptionEN = a['strDescriptionEN']
            except KeyError:
                newalb.strDescriptionEN = ''
            newalb.strArtist = a['strArtist']
            newalb.idArtist = a['idArtist']
            if a['strAlbumThumb']:
                newalb.strAlbumThumb = a['strAlbumThumb']
            else:
                newalb.strAlbumThumb = ''
            if a['intYearReleased']:
                newalb.intYearReleased = a['intYearReleased']
            else: 
                newalb.intYearReleased = ''
            if a['strLabel']:
                newalb.strLabel = a['strLabel']
            else: 
                newalb.strLabel = ''
            if a['strGenre']:
                newalb.strGenre = a['strGenre']
            else:
                newalb.strGenre = ''
            newalb.save()
    
        # add nomination
        nom = Nomination()
        nom.album = newalb
        nom.user = user
        nom.save()

def remove_nomination(user, album_id):    
    album = Album.objects.get(id=album_id)
    nomination = Nomination.objects.filter(user=user, album=album).first()
    nomination.delete()      