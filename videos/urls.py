from django.urls import path, include
from rest_framework.routers import DefaultRouter
from videos.views import HomeVidoes, UserVidoes, VideoViewSet, PublishVideo,GetSavedVideo, SaveLater
from .upload_media import FileUploadView

router = DefaultRouter()
router.register(r'videos', VideoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('home_videos', HomeVidoes.as_view()),

    path('publish_video', PublishVideo.as_view()),
    path('save_for_later', SaveLater.as_view()),

    path(r'get_saved_video', GetSavedVideo.as_view())
]