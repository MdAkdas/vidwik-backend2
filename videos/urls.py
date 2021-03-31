from django.urls import path
from videos.views import PublishVideo, SavedVideoDetails, SaveVideo, ForkVideo, UserVideos, UpdateSavedVideo,EditForkVideo

urlpatterns = [
    path('publish_video', PublishVideo.as_view()),
    path('save_video', SaveVideo.as_view()),
    path(r'video_details', SavedVideoDetails.as_view()),
    path('update_video', UpdateSavedVideo.as_view()),
    path('fork_video', ForkVideo.as_view()),
    path('user_videos', UserVideos.as_view()),
    path('edit_fork_video', EditForkVideo.as_view())
]
