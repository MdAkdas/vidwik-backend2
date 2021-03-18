from django.db import models
from user.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


# PublishedVideo , SavedVideo
class Tags(models.Model):
    tag_text = models.CharField(max_length=200, null=True, blank=True)


# has user, tag
class PublishedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # FK?
    tags = models.ManyToManyField(Tags)
    # media_details = models.OneToOneField(MediaDetails, on_delete=models.CASCADE, default=None, null=True,
    #                                      blank=True)  # OTOF?
    # collaborate =

    title = models.CharField(max_length=100)
    thumbnail = models.FileField(upload_to='publish/%Y/%m/%d/thumbnail', default=None, null=True)
    gif = models.FileField(upload_to='publish/gifs/%Y/%m/%d/video', default=None, null=True)
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
    tags = models.ManyToManyField(Tags)
    # media detail(like, share) not required for saved video?
    # media_library

    is_paid = models.BooleanField(default=False, blank=True, null=True)
    is_published = models.BooleanField(default=False, blank=True, null=True)  # why?
    title = models.CharField(max_length=100)
    thumbnail = models.FileField(upload_to='saved/%Y/%m/%d/thumbnail', default=None, null=True)
    gif = models.FileField(upload_to='saved/gifs/%Y/%m/%d/video', default=None, null=True)
    video_file = models.FileField(upload_to='saved/%Y/%m/%d/video', default=None, null=True)
    created_at = models.DateTimeField(default=timezone.datetime.utcnow, blank=True, null=True)
    description = models.TextField(null=True)
    duration = models.TimeField(default=timezone.datetime.utcnow, null=True)
    published_video_details = models.OneToOneField(PublishedVideo, on_delete=models.DO_NOTHING)

    bg_musicfile = models.FileField(upload_to='saved/bgms/%Y/%m/%d/video', default=None, null=True)
    # scene id
    # audio_id =



# <- saved video
# has subtitle and media and audio
class Scenes(models.Model):
    video = models.ForeignKey(SavedVideo, on_delete=models.CASCADE)  # FK?
    order = models.IntegerField(default=1, null=True, blank=True)
    title = models.TextField(null=True, blank=True, default="")
    animation = models.CharField(max_length=200, null=True, blank=True) #todo
    narration = models.FileField(upload_to='saved/narrations/%Y/%m/%d/video', default=None, null=True)
    # audio id
    # subtitle
    # media
    #keyword in scene #todo


# <-scenes
#has media
class Subtitle(models.Model):
    scene = models.OneToOneField(Scenes, on_delete=models.CASCADE)

    alignment_types = (
        ("Left", "left"),
        ("Right", "right"),
    )
    alignment = models.CharField(max_length=6, choices=alignment_types)
    font_color = models.CharField(max_length=6)
    background_color = models.CharField(max_length=6)

    text_position_types = (
        ("Top", "top"),
        ("Center", "center"),
        ("Bottom", "bottom")
    )
    text_position = models.CharField(max_length=10, choices=text_position_types)
    # layout ??
    # animation = models.CharField(max_length=200, null=True, blank=True) ??

    # content ? txt?
    subtitle_text = models.TextField(null=True, blank=True, default="")
    font_style = models.CharField(max_length=50)
    font_size = models.IntegerField()  # ?
    font_type = models.CharField(max_length=50)


# <- scenes
# media = scene's video. uploaded or from library
#todo how to connect media to media lib. there are some common fields
class Media(models.Model):
    # type
    scene = models.OneToOneField(Scenes, on_delete=models.CASCADE)

    media_types = (
        ("Upload", "upload"),
        ("Library", "library")
    )
    type = models.CharField(max_length=10, choices=media_types)
    media_file = models.FileField(upload_to='scenes/user_uploaded_video/%Y/%m/%d', blank=True, null=True)
    item_duration = models.TimeField(default=timezone.datetime.utcnow, null=True)
    # media_library ??

# # <- scenes and saved video ?
#
# # has media lib
# class Audio(models.Model):
#     scene = models.ForeignKey(SavedVideo, on_delete=models.CASCADE)  # FK / OTOF?
#     audio_file = models.FileField(upload_to='saved/audio/%Y/%m/%d/video', default=None, null=True)
#     audio_types = (
#         ("Uploaded", "uploaded"),
#         ("Library", "library"),
#         ("Narration", "narration")
#     )
#     audio_type = models.CharField(max_length=10, choices=audio_types)
#
#
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
