from django.contrib import admin
from .models import PublishedVideo,Tags, SavedVideo, Scenes,Media,Subtitle, Audio, Fork
# Register your models here.

@admin.register(PublishedVideo)
class PublishedVideoAdmin(admin.ModelAdmin):
    list_display = ('id','title',)


@admin.register(SavedVideo)
class SavedVideoAdmin(admin.ModelAdmin):
    list_display = ('id','title',)


@admin.register(Fork)
class SavedVideoAdmin(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ('id',)



@admin.register(Scenes)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(Media)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id','tag_text')