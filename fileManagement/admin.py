from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display=['id','name', 'parent_folder']
    
@admin.register(File)
class FolderAdmin(admin.ModelAdmin):
    list_display=['id', 'name','file_type','file','folder','created_at','user']   

 