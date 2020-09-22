from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Album, Nomination, Review
from .forms import ReviewForm, AlbumForm
from .methods import addalbum, nominate, remove_nomination

import requests


def index(request):
    user = request.user
    can_review = True
     # Get current AOTW
    try:
        aotw = Nomination.objects.get(active=True)
        
    except Nomination.DoesNotExist:
        aotw = None        

    ## Upcoming Nominations
    nominations = Nomination.objects.filter(aotw=False)
    # Past Nominations
    pastnoms = Nomination.objects.filter(aotw=True, active=False)
    # Is user an admin?
    if user.groups.filter(name="leader").exists():
        leader = True
    else:
        leader = False

    # Reviews
    if aotw: 
        reviews = Review.objects.filter(album=aotw.album.id)
        
        album = Album.objects.get(id=aotw.album.id)
        score = 0
        # Calculate average rating
        if len(reviews) > 0:
            for review in reviews:
                score += review.rating 
            score = score/len(reviews)      
            album.score = score
            album.save()       
    # Review Form
        
        if user.is_authenticated:
            try:
                reviews.get(user=user)
            except NameError:
                can_review = True
            else:
                can_review = False

        form = ReviewForm(request.POST or None)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = user
            review.save()
            return HttpResponseRedirect(reverse("index"))

    return render(request, "aotw/index.html", {
        "aotw": aotw,
        "nominations": nominations,
        "pastnoms": pastnoms,
        "form": form, 
        "can_review": can_review,
        "reviews": reviews,
        "score": score, 
        "leader": leader
    })   


def search(request):
    if request.method == "POST":
        search_type = request.POST["search-option"]
        query = request.POST["search"]

        return HttpResponseRedirect(reverse("albumsearch", args=[search_type, query]))
               
    return render(request, "aotw/search.html")
  
    
def albumsearch(request, search_type, query):
    message = ""
    form = AlbumForm(request.POST or None)
    if form.is_valid():
        album = form.save(commit=False)
        addalbum(album)
        message = "Album saved!"

    albums = []
    if search_type == '1':
        albums = Album.objects.filter(strArtist__iexact=query, custom=True)
        albums = list(albums)
        response = requests.get('https://www.theaudiodb.com/api/v1/json/1/searchalbum.php?s=%s' % query)
        response = response.json()
        if response['album'] != None:
            albums += response['album']            
                    
    elif search_type == '2':
        albums = Album.objects.filter(strAlbum__iexact=query, custom=True)
        albums = list(albums)
        response = requests.get('https://www.theaudiodb.com/api/v1/json/1/searchalbum.php?a=%s' % query)
        response = response.json()
        if response['album'] != None: 
            albums += response['album']            

    if albums: 
        paginator = Paginator(albums, 9) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)                
     
        return render(request, "aotw/searchresults.html", {
            'results': len(albums),
            'albums': albums,
            'page_obj': page_obj, 
            'form': form,
            'message': message })

    else: 
        return render(request, "aotw/searchresults.html", {
            'albums': albums,
             'form': form})


def album(request, album_id):
    
    ## if album in database, read from db
    try:
        album = Album.objects.get(idAlbum=album_id)
        score = album.score
        reviews = Review.objects.filter(album=album.id)
        ## check if nominated
        try: 
            nomination = Nomination.objects.get(album=album.id)
        except Nomination.DoesNotExist:
            nomination = None       
             

    except Album.DoesNotExist:
        ## if album NOT in database, get from API
        response = requests.get('https://theaudiodb.com/api/v1/json/1/album.php?m=%s' % album_id)
        response = response.json()
        album = response['album'][0]
        score = None
        reviews = None
        nomination = None

    return render(request, "aotw/album.html", {
        "a": album,
        "nomination": nomination,
        "reviews": reviews,
        "score": score
        })     


def artist(request, artist_id):
    ##always get from API
    response = requests.get('https://theaudiodb.com/api/v1/json/1/artist.php?i=%s' % artist_id)
    response = response.json()
    artists = response['artists']

    return render(request, "aotw/artist.html", {"artists": artists})

       
@login_required    
def nominations(request):
    ## render all nominations
    user = request.user
    if request.method == 'POST':
        if 'remove' in request.POST:
            album_id = request.POST["remove"]
            album = Album.objects.get(id=album_id)
            remove_nomination(user, album.id)

            return HttpResponseRedirect(reverse("nominations"))

        if 'newnom' in request.POST:
            album_id = request.POST["newnom"]
            nominate(user, album_id) 

            return HttpResponseRedirect(reverse("nominations"))   
    
    else: 
        nominations = Nomination.objects.filter(aotw=False)
        return render(request, "aotw/nominations.html", {
        "nominations": nominations,
        "user": user
    })
    return HttpResponseRedirect(reverse("nominations"))


@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    current_user = request.user
    
    if request.method == 'POST':
        album_id = request.POST["remove"]
        remove_nomination(current_user, album_id)
    
    nominations = Nomination.objects.filter(user=user)
    reviews = Review.objects.filter(user=user)
    return render(request, "aotw/profile.html", {
        "user": user,
        "current_user": current_user,
        "nominations": nominations,
        "reviews": reviews,
    })


@login_required
def adminpage(request):
    ## Check if admin
    if request.user.groups.filter(name="leader").exists():
        ## Current AOTW
        try:
            aotw = Nomination.objects.get(active=True)
        except Nomination.DoesNotExist:
            aotw = None
        
        ## Upcoming Nominations
        nominations = Nomination.objects.filter(aotw=False)

        ## Past Nominations
        pastnoms = Nomination.objects.filter(aotw=True, active=False)

        # Custom Nomination form
        form = AlbumForm(request.POST or None)
        if form.is_valid():
            album = form.save(commit=False)
            addalbum(album)
            return HttpResponseRedirect(reverse("adminpage"))

        # Listen for promotion to AOTW
        if request.method == "POST":
            if 'promote' in request.POST:
            # remove old active AOTW
                if aotw:            
                    aotw.active = False
                    aotw.save()

            # promote new AOTW
                new_aotw = request.POST["promote"]
                new_aotw = Nomination.objects.get(album=new_aotw)
                new_aotw.aotw = True
                new_aotw.active = True
                new_aotw.save()

                return HttpResponseRedirect(reverse("adminpage"))

        return render(request, "aotw/adminpage.html", {
            "aotw": aotw,
            "nominations": nominations,
            "pastnoms": pastnoms,
            "form": form
        }) 
    else:
        return HttpResponseRedirect(reverse("index"))

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


