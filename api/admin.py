from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(On_Live)
class Onlive(admin.ModelAdmin):
    pass


@admin.register(Vtuber)
class Vtuber(admin.ModelAdmin):
    pass