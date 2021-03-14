from django.db import models
from user.models import User
from django.utils import timezone


class MediaDetails(models.Model):
    pass


class Collaborate(models.Model):
    pass


class PublishedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # FK?
    # tags
    media_details = models.OneToOneField(MediaDetails, on_delete=models.CASCADE, default=None, null=True,
                                         blank=True)  # OTOF?
    # collaborate =

    title = models.CharField(max_length=100)
    thumbnail = models.FileField(upload_to='publish/%Y/%m/%d/thumbnail', default=None, null=True)
    gif = models.FileField(upload_to='publish/gifs/%Y/%m/%d/video', default=None, null=True)
    video_file = models.FileField(upload_to='publish/%Y/%m/%d/video', default=None, null=True)
    publish_at = models.DateTimeField(default=timezone.datetime.utcnow, blank=True, null=True)
    description = models.TextField(null=True)
    duration = models.TimeField(default=timezone.datetime.utcnow, null=True)
    is_published = models.BooleanField(default=False, blank=True, null=True)  # why?
    is_paid = models.BooleanField(default=False, blank=True, null=True)


class SavedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # tags
    media_details = models.OneToOneField(MediaDetails, on_delete=models.CASCADE, default=None, null=True,
                                         blank=True)  # OTOF?
    # media_library
    # published_video

    is_paid = models.BooleanField(default=False, blank=True, null=True)
    is_published = models.BooleanField(default=False, blank=True, null=True)  # why?
    title = models.CharField(max_length=100)
    thumbnail = models.FileField(upload_to='saved/%Y/%m/%d/thumbnail', default=None, null=True)
    gif = models.FileField(upload_to='saved/gifs/%Y/%m/%d/video', default=None, null=True)
    video_file = models.FileField(upload_to='saved/%Y/%m/%d/video', default=None, null=True)
    created_at = models.DateTimeField(default=timezone.datetime.utcnow, blank=True, null=True)
    description = models.TextField(null=True)
    duration = models.TimeField(default=timezone.datetime.utcnow, null=True)

    # scene id
    # audio_id =


class Scenes(models.Model):
    video = models.ForeignKey(SavedVideo, on_delete=models.CASCADE)  # FK?
    order = models.IntegerField(default=1, null=True, blank=True)
    title = models.TextField(null=True, blank=True, default="")

    # audio id
    # subtitle
    # media


class Audio(models.Model):
    scene = models.ForeignKey(SavedVideo, on_delete=models.CASCADE)  # FK?

    pass


class Subtitle(models.Model):
    scene = models.ForeignKey(Scenes, on_delete=models.CASCADE)

    alignment_types = (
        ("Left", "left"),
        ("Right", "right"),
    )
    alignment = models.CharField(choices=alignment_types)
    font_color = models.CharField(max_length=6)
    background_color = models.CharField(max_length=6)

    text_position_types = (
        ("Top", "top"),
        ("Center", "center"),
        ("Bottom", "bottom")
    )
    text_postion = models.CharField(choices=text_position_types)
    # layout
    # animation = models.CharField(max_length=200, null=True, blank=True)
    # content ? txt?
    font_style = models.CharField(max_length=50)
    font_size = models.IntegerField(max_length=30) #?
    font_type = models.CharField(max_length=50)



class Media(models.Model):
    # type
    media_types = (
        ("Upload", "upload"),
        ("Library", "library")
    )
    type = models.CharField(choices=media_types)
    media_file = models.FileField(upload_to='scenes/user_uploaded_video/%Y/%m/%d', blank=True, null=True)
    item_duration = models.TimeField(default=timezone.datetime.utcnow, null=True)
    animation = models.CharField(max_length=200, null=True, blank=True)
    # media_library ??


class MediaLibrary(models.Model):
    pass


class TemporaryFiles(models.Model):
    created_at = models.DateTimeField(default=timezone.datetime.utcnow)
    temp_file = models.FileField(upload_to="temporary/%Y/%m/%d")


class Tags(models.Model):
    tag_text = models.CharField(max_length=200, null=True, blank=True)
    videos = models.ManyToManyField(PublishedVideo)

#
# class Scenes(models.Model):
#     order = models.IntegerField(default=1, null=True, blank=True)
#     video_url = models.URLField(default=None, null=True, blank=True)
#     video_file = models.FileField(upload_to='scenes/user_uploaded_video/%Y/%m/%d', blank=True, null=True)
#     text = models.TextField(null=True, blank=True, default="")
#     keywords = models.TextField(null=True, blank=True, default="")
#     font_color = models.CharField(max_length=10, default="#000000", null=True, blank=True)
#     background_color = models.CharField(max_length=10, default="#ffffff", null=True, blank=True)
#     text_position = models.CharField(max_length=10, default="bottom", null=True, blank=True)
#     narration = models.FileField(upload_to='scenes/user_uploaded_narration/%Y/%m/%d', blank=True, null=True)
#     video = models.ForeignKey(Video, on_delete=models.CASCADE, default=None, null=True, blank=True)
