from django.urls import path, include
from rest_framework.routers import DefaultRouter
from videos.views import PublishVideo,SavedVideoDetails, SaveVideo, ForkVideo, UserVideos, UpdateSavedVideo
from .upload_media import FileUploadView


urlpatterns = [
    # path('home_videos', HomeVidoes.as_view()),
    path('publish_video', PublishVideo.as_view()),
    path('save_video', SaveVideo.as_view()),
    path(r'saved_video_details', SavedVideoDetails.as_view()),
    path('update_video', UpdateSavedVideo.as_view()),
    path('fork_video', ForkVideo.as_view()),
    path('user_videos', UserVideos.as_view())
]