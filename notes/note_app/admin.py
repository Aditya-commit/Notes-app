from django.contrib import admin

# Register your models here.

from .models import User,Note

@admin.register(User)
class useradmin(admin.ModelAdmin):
	list_display=['username','name','email','password']

@admin.register(Note)
class Noteadmin(admin.ModelAdmin):
	list_display=['id','username','title','text']