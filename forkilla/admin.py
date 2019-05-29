from django.contrib import admin
from .models import Review, Profile, Reservation, Restaurant

# Register your models here.

admin.site.register(Profile)
admin.site.register(Reservation)
admin.site.register(Restaurant)
admin.site.register(Review)