from django.db import models
from user.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


#
# class Collaborate(models.Model):
#     pass


# has user, tag, collab, media detail
class PublishedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # FK?
    # tags in scene or in video
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


class MediaDetails(models.Model):
    video = models.ForeignKey(PublishedVideo,on_delete=models.CASCADE)
    overall_rating = models.IntegerField(default=4, validators=[MinValueValidator(0),MaxValueValidator(5)])
    no_of_shares = models.IntegerField(default=0)
    views = models.IntegerField(default=1)


#
# # has user,tag, media detail, media lib, published video
# # audio and scene
# class SavedVideo(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     # tags
#     media_details = models.OneToOneField(MediaDetails, on_delete=models.CASCADE, default=None, null=True,
#                                          blank=True)  # OTOF?
#     # media_library
#     # published_video ??
#
#     is_paid = models.BooleanField(default=False, blank=True, null=True)
#     is_published = models.BooleanField(default=False, blank=True, null=True)  # why?
#     title = models.CharField(max_length=100)
#     thumbnail = models.FileField(upload_to='saved/%Y/%m/%d/thumbnail', default=None, null=True)
#     gif = models.FileField(upload_to='saved/gifs/%Y/%m/%d/video', default=None, null=True)
#     video_file = models.FileField(upload_to='saved/%Y/%m/%d/video', default=None, null=True)
#     created_at = models.DateTimeField(default=timezone.datetime.utcnow, blank=True, null=True)
#     description = models.TextField(null=True)
#     duration = models.TimeField(default=timezone.datetime.utcnow, null=True)
#
#     # scene id
#     # audio_id =
#
#
#
# # <- saved video
# # has subtitle and media and audio
# class Scenes(models.Model):
#     video = models.ForeignKey(SavedVideo, on_delete=models.CASCADE)  # FK?
#     order = models.IntegerField(default=1, null=True, blank=True)
#     title = models.TextField(null=True, blank=True, default="")
#
#     # audio id
#     # subtitle
#     # media
#
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
#
# # <-scenes
# #has media
# class Subtitle(models.Model):
#     scene = models.ForeignKey(Scenes, on_delete=models.CASCADE)
#
#     alignment_types = (
#         ("Left", "left"),
#         ("Right", "right"),
#     )
#     alignment = models.CharField(max_length=6, choices=alignment_types)
#     font_color = models.CharField(max_length=6)
#     background_color = models.CharField(max_length=6)
#
#     text_position_types = (
#         ("Top", "top"),
#         ("Center", "center"),
#         ("Bottom", "bottom")
#     )
#     text_postion = models.CharField(max_length=10, choices=text_position_types)
#     # layout
#     # animation = models.CharField(max_length=200, null=True, blank=True)
#     # content ? txt?
#     font_style = models.CharField(max_length=50)
#     font_size = models.IntegerField()  # ?
#     font_type = models.CharField(max_length=50)
#
# # <- scenes
# class Media(models.Model):
#     # type
#     media_types = (
#         ("Upload", "upload"),
#         ("Library", "library")
#     )
#     type = models.CharField(max_length=10, choices=media_types)
#     media_file = models.FileField(upload_to='scenes/user_uploaded_video/%Y/%m/%d', blank=True, null=True)
#     item_duration = models.TimeField(default=timezone.datetime.utcnow, null=True)
#     animation = models.CharField(max_length=200, null=True, blank=True)
#     # media_library ??

# PublishedVideo , SavedVideo
class Tags(models.Model):
    tag_text = models.CharField(max_length=200, null=True, blank=True)
    videos = models.ManyToManyField(PublishedVideo) #how to add savedVideo model

#
# class TemporaryFiles(models.Model):
#     created_at = models.DateTimeField(default=timezone.datetime.utcnow)
#     temp_file = models.FileField(upload_to="temporary/%Y/%m/%d")
