from django.contrib import admin
from .models import PublishedVideo,Tags, SavedVideo, Scenes,Media, MediaDetails,Subtitle
# Register your models here.

@admin.register(PublishedVideo)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id','title',)


admin.register(SavedVideo)


admin.register(MediaDetails)


admin.register(Subtitle)



admin.register(Scenes)



admin.register(Media)




#
# @admin.register(Scenes)
# class ScencesAdmin(admin.ModelAdmin):
#     list_display = ('id','video',)

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id',)