from pyexpat.errors import messages
from django.contrib.auth.models import User
from django.contrib import admin
from .models import Image, Folder
import os

    
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):  # Säädetään, mitä admin imagen sivustolla näytetään ja voi tehdä.
    list_display = ('user','image_title', 'description', 'upload_date', 'id')
    list_filter = ['upload_date']
    search_fields = ['image_title', 'upload_date']
    
@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):  # Säädetään, mitä admin imagen sivustolla näytetään ja voi tehdä.
    list_display = ('name', 'user', 'id')
    list_filter = ['id']
    search_fields = ['name', 'user']
    