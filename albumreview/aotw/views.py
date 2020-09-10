from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User

import requests


def index(request):
    return render(request, "aotw/index.html")


def search(request):            
    return render(request, "aotw/search.html")


def artistsearch(request, artist):
    response = requests.get('https://www.theaudiodb.com/api/v1/json/523532/searchalbum.php?s=%s' % artist)
    response = response.json()
    albums = response['album']            
    return render(request, "aotw/searchresults.html", {"albums": albums})


def albumsearch(request, album):
    response = requests.get('https://www.theaudiodb.com/api/v1/json/1/searchalbum.php?a=%s' % album)
    response = response.json()
    albums = response['album']            
    return render(request, "aotw/searchresults.html", {"albums": albums})


def album(request, album_id):
    response = requests.get('https://theaudiodb.com/api/v1/json/1/album.php?m=%s' % album_id)
    response = response.json()
    album = response['album']
    
    return render(request, "aotw/album.html", {"album": album})     


def nominate(request, album_id):
    return HttpResponseRedirect(reverse("nominations"))
    
def nominations(request):
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
