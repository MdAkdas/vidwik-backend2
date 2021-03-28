from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from videos.models import PublishedVideo
from .workingAPI import publish_api, get_video_details, save_video, update_saved_video
from .send_mail import sendMail
from .models import PublishedVideo, User, SavedVideo, Fork
from rest_framework import status


class PublishVideo(APIView):
    def post(self, request):
        return publish_api.publish(request)


class SaveVideo(APIView):
    def post(self, request):
        return save_video.save(request)


class SavedVideoDetails(APIView):
    def get(self, request):
        # what if user want to update the publish video only
        if request.GET.get("published_video_id") != None:
            save_video = SavedVideo.objects.get(published_video_id=request.GET.get("published_video_id"))
            save_video_id = save_video.id

        else:
            save_video_id = request.GET.get("saved_video_id")

        print(save_video_id)
        return get_video_details.get_video(str(save_video_id))

        # id = request.GET.get("id")
        # print(id)
        # return get_video_details.get_video(id)


class UpdateSavedVideo(APIView):
    def post(self, request):
        return update_saved_video.update_video.save(request)


class ForkVideo(APIView):
    def get(self, request):
        username = request.GET.get("user")
        published_video_id = request.GET.get("published_video_id")

        user_pk = User.objects.get(username=username)
        print(user_pk)
        publish_pk = PublishedVideo.objects.get(id=published_video_id)
        print(publish_pk)
        new_forked = Fork.objects.create(user=user_pk, published_video=publish_pk)
        return JsonResponse(
            {"message": "Forked Successfully", "id": new_forked.id, "status": status.HTTP_201_CREATED})


#
#
# class EditVideo(APIView):
#     def get(self, request):
#         forked_video_id = request.GET.get("published_video_id")
#         print(forked_video_id)
#         save_video_id = SavedVideo.objects.get(published_video_id=forked_video_id)
#         print(save_video_id.id)
#         return get_video_details.get_video(str(save_video_id.id))


# edit for saved video ?
# user token

class UserVideos(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.method == 'GET':
            username = request.GET.get("user")
            print(username)
            user_pk = User.objects.get(username=username)
            print(user_pk)

            videos = {
                'published_video': list(PublishedVideo.objects.filter(user=user_pk).values(
                    'id', 'user__username', 'title', 'description', 'thumbnail', 'video_file',
                    'user__first_name', 'user__last_name',
                    'published_at', 'duration', 'is_published'
                )),
                'saved_video': list(SavedVideo.objects.filter(user=user_pk).values(
                    'id', 'user__username', 'title', 'description', 'thumbnail', 'video_file',
                    'user__first_name', 'user__last_name',
                    'created_at', 'duration', 'is_published'
                )),

                'forked_video': list(Fork.objects.filter(user=user_pk).values(
                    'id', 'published_video__title', 'user__username', 'published_video__description',
                    'published_video__thumbnail',
                    'published_video__video_file',
                    'user__first_name', 'user__last_name',
                    'published_video__published_at', 'published_video__duration', 'published_video__is_paid'
                )),
            }

            return JsonResponse(videos)

# Do it through authenticated user.
