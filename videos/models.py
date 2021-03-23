from django.db import models
from user.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from musicLibrary.models import MusicLib

# PublishedVideo , SavedVideo
class Tags(models.Model):
    tag_text = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.tag_text


# has user, tag
class PublishedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # FK?
    tags = models.ManyToManyField(Tags,blank=True)

    title = models.CharField(max_length=100)
    thumbnail = models.FileField(upload_to='publish/%Y/%m/%d/thumbnail', default=None, null=True)
    gif = models.FileField(upload_to='publish/gifs/%Y/%m/%d/gif', default=None, null=True)
    video_file = models.FileField(upload_to='publish/%Y/%m/%d/video', default=None, null=True)
    published_at = models.DateTimeField(default=timezone.datetime.utcnow, blank=True, null=True)
    description = models.TextField(null=True)
    duration = models.TimeField(default=timezone.datetime.utcnow, null=True)
    is_published = models.BooleanField(default=False, blank=True, null=True)  # why?
    is_paid = models.BooleanField(default=False, blank=True, null=True)



# has user,tag, media detail, media lib, published video
# audio and scene
class SavedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tags,blank=True)
    # media detail(like, share) not required for saved video?
    # media_library

    #for bg music
    music_lib = models.ForeignKey(MusicLib, on_delete=models.DO_NOTHING, null=True)

    is_paid = models.BooleanField(default=False, blank=True, null=True)
    is_published = models.BooleanField(default=False, blank=True, null=True)
    title = models.CharField(max_length=100)
    thumbnail = models.FileField(upload_to='saved/%Y/%m/%d/thumbnail', default=None, null=True)
    gif = models.FileField(upload_to='saved/%Y/%m/%d/gifs', default=None, null=True)
    video_file = models.FileField(upload_to='saved/%Y/%m/%d/video', default=None, null=True)
    created_at = models.DateTimeField(default=timezone.datetime.utcnow, blank=True, null=True)
    description = models.TextField(null=True)
    duration = models.TimeField(default=timezone.datetime.utcnow, null=True)
    published_video = models.OneToOneField(PublishedVideo, on_delete=models.DO_NOTHING, null=True, blank=True)




# <- saved video
# has subtitle and media and audio
class Scenes(models.Model):
    video = models.ForeignKey(SavedVideo, on_delete=models.CASCADE)  # FK?
    order = models.IntegerField(default=1, null=True, blank=True)
    title = models.TextField(null=True, blank=True, default="")
    # transition type?
    transition = models.CharField(max_length=200, null=True, blank=True) #todo
    tags = models.ManyToManyField(Tags,blank=True)



# <-scenes
class Subtitle(models.Model):
    scene = models.OneToOneField(Scenes, on_delete=models.CASCADE)

    alignment_types = (
        ("Left", "left"),
        ("Right", "right"),
    )
    alignment = models.CharField(max_length=6, choices=alignment_types)
    font_color = models.CharField(max_length=7)
    background_color = models.CharField(max_length=7)

    text_position_types = (
        ("Top", "top"),
        ("Center", "center"),
        ("Bottom", "bottom")
    )
    text_position = models.CharField(max_length=10, choices=text_position_types)
    # layout ??
    # animation = models.CharField(max_length=200, null=True, blank=True) ??

    # content ? txt?
    text = models.TextField(null=True, blank=True, default="")
    font_style = models.CharField(max_length=50)
    font_size = models.IntegerField()  # ?
    font_type = models.CharField(max_length=50)


# <- scenes
# media = scene's video. uploaded or from library
#For video and images
class Media(models.Model):
    # type
    scene = models.OneToOneField(Scenes, on_delete=models.CASCADE)

    med_types = (
        ("Upload", "upload"),
        ("Library", "library")
    )
    media_type = models.CharField(max_length=10, choices=med_types)
    media_file = models.FileField(upload_to='scenes/media/%Y/%m/%d', blank=True, null=True)
    item_duration = models.TimeField(default=timezone.datetime.utcnow, null=True)

    cont_types = (
        ("Video", "video"),
        ("Image", "image")
    )
    content_type = models.CharField(max_length=10, choices=cont_types)

    animation_type = (
        ("None","none"),
        ("Zoom In","zoom in"),
        ("Zoom Out","zoom out")
    )
    animation = models.CharField(max_length=30,choices=animation_type, null=True)

# <- scene
class Audio(models.Model):
    scene = models.OneToOneField(Scenes, on_delete=models.CASCADE)
    aud_types = (
        ("Upload", "upload"),
        ("Narration", "narration")
    )
    audio_type = models.CharField(max_length=20,choices=aud_types)
    audio_file = models.FileField(upload_to='saved/audio/%Y/%m/%d/video', default=None, null=True)



# # <- Audio
# class MediaLibrary(models.Model):
#     pass

# todo for later
# class MediaDetails(models.Model):
#     video = models.OneToOneField(PublishedVideo,on_delete=models.CASCADE)
#     overall_rating = models.IntegerField(default=4, validators=[MinValueValidator(0),MaxValueValidator(5)])
#     no_of_shares = models.IntegerField(default=0)
#     views = models.IntegerField(default=1)


#
# class TemporaryFiles(models.Model):
#     created_at = models.DateTimeField(default=timezone.datetime.utcnow)
#     temp_file = models.FileField(upload_to="temporary/%Y/%m/%d")
