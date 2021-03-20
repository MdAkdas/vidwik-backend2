from django.urls import path, include
from rest_framework.routers import DefaultRouter
from videos.views import PublishVideo,GetSavedVideo, SaveLater
from .upload_media import FileUploadView


urlpatterns = [
    # path('home_videos', HomeVidoes.as_view()),

    path('publish_video', PublishVideo.as_view()),
    path('save_video', SaveLater.as_view()),
    path(r'get_saved_video', GetSavedVideo.as_view())
]