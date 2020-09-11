from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("search", views.search, name="search"),
    path("search/<str:search_type>/<str:query>", views.albumsearch, name="albumsearch"),
    path("album/<str:album_id>", views.album, name="album"),
    path("artist/<str:artist_id>", views.artist, name="artist"),
    path("nominate/<str:album_id>", views.nominate, name="nominate"),
    path("nominations", views.nominations, name="nominations")
]

