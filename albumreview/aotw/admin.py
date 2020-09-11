from django.contrib import admin
from .models import User, Album, Nomination, Review

# Register your models here.
admin.site.register(User)
admin.site.register(Album)
admin.site.register(Nomination)
admin.site.register(Review)