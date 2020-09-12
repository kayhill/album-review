from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Album, Nomination, Review

import requests


def index(request):
    return render(request, "aotw/index.html")


def search(request):
    if request.method == "POST":
        search_type = request.POST["search-option"]
        query = request.POST["search"]
        return HttpResponseRedirect(reverse("albumsearch", args=[search_type, query]))
               
    return render(request, "aotw/search.html")


def albumsearch(request, search_type, query):
    if request.method == "POST":
        search_type = request.POST["search-option"]
        query = request.POST["search"]
        return HttpResponseRedirect(reverse("albumsearch", args=[search_type, query]))        
    else:
        albums = {}
        if search_type == '1':
            response = requests.get('https://www.theaudiodb.com/api/v1/json/1/searchalbum.php?s=%s' % query)
            response = response.json()
            albums = response['album']
        
        elif search_type == '2':
            response = requests.get('https://www.theaudiodb.com/api/v1/json/1/searchalbum.php?a=%s' % query)
            response = response.json()
            albums = response['album']
        
        if albums: 
            paginator = Paginator(albums, 9) 
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)            
        
            return render(request, "aotw/searchresults.html", {
                    'results': len(albums),
                    'albums': albums,
                    'page_obj': page_obj})

        else: 
            return render(request, "aotw/searchresults.html", {
                'albums': albums})


def album(request, album_id):
    ## if album in database, read from db

    ## check if nominated

    ## if album NOT in database, get from API
    response = requests.get('https://theaudiodb.com/api/v1/json/1/album.php?m=%s' % album_id)
    response = response.json()
    album = response['album']
    return render(request, "aotw/album.html", {"album": album})     

def artist(request, artist_id):
    ##always get from API
    response = requests.get('https://theaudiodb.com/api/v1/json/1/artist.php?i=%s' % artist_id)
    response = response.json()
    artists = response['artists']

    return render(request, "aotw/artist.html", {"artists": artists})

def nominate(request, album_id):
    ## check if album in db
    

    ## save to db
    return HttpResponseRedirect(reverse("nominations"))
    
def nominations(request):
    ## render all nominations
    return render(request, "aotw/nominations.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "aotw/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "aotw/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "aotw/register.html")


def login_view(request):    
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "aotw/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "aotw/login.html")


def logout_view(request):    
    logout(request)
    return HttpResponseRedirect(reverse("index"))
