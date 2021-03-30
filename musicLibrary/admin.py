from django.contrib import admin
from .models import MusicLib

# Register your models here.

@admin.register(MusicLib)
class MusicLibAdmin(admin.ModelAdmin):
    list_display = ('id','title',)
