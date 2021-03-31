from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from videos.models import PublishedVideo
from .workingAPI import publish_api, get_video_details, save_video, update_saved_video
from .send_mail import sendMail
from .models import PublishedVideo, User, SavedVideo, Fork
from rest_framework import status


class PublishVideo(APIView):
    def post(self, request):
        # save then publish

        # {"Message":"Video Saved Successfully.","id":42,"status":201}
        save_response = save_video.save(request)
        print("save response: ",save_response)
        save_video_id = save_response["id"]
        if save_response["status"] == 201:
            publish_response = publish_api.publish(request)
            published_id = publish_response["id"]
            print("publish response: ", publish_response)

            if publish_response["status"] == 201:
                SavedVideo.objects.filter(id=save_video_id).update(is_published=True, published_id=publish_response["id"])
                return Response(publish_response)

            else:
                SavedVideo.objects.get(id=save_video_id).delete()
                PublishedVideo.objects.get(id=published_id).delete()
                return Response({"Message": publish_response["Message"], "status": status.HTTP_400_BAD_REQUEST})
        else:
            SavedVideo.objects.get(id=save_video_id).delete()
            return Response({"Message": save_response["Message"], "status": status.HTTP_400_BAD_REQUEST})


class SaveVideo(APIView):
    def post(self, request):
        response_dict = save_video.save(request)
        return Response(response_dict)


class SavedVideoDetails(APIView):
    def get(self, request):
        # what if user want to update the publish video only
        print("published_id", request.GET.get("published_id"))

        if request.GET.get("published_id") != 'None':
            print("published_id", request.GET.get("published_id"))
            save_video = SavedVideo.objects.get(published_id=request.GET.get("published_id"))
            save_video_id = save_video.id

        else:
            print("saved_video_id",request.GET.get("saved_video_id"))
            save_video_id = request.GET.get("saved_video_id")

        print(save_video_id)
        return get_video_details.get_video(str(save_video_id))

        # id = request.GET.get("id")
        # print(id)
        # return get_video_details.get_video(id)


class UpdateSavedVideo(APIView):
    def post(self, request):
        return update_saved_video.update_video(request)


class ForkVideo(APIView):
    def get(self, request):
        user_id = request.GET.get("user_id")
        published_id = request.GET.get("published_id")

        user_pk = User.objects.get(id=user_id)
        print(user_pk)
        publish_pk = PublishedVideo.objects.get(id=published_id)
        print(publish_pk)
        new_forked = Fork.objects.create(user=user_pk, published_id=publish_pk)
        return JsonResponse(
            {"message": "Forked Successfully", "id": new_forked.id, "status": status.HTTP_201_CREATED})




class EditForkVideo(APIView):
    def get(self, request):
        print("in edit_fork_video")
        fork_id = request.GET.get("fork_id")
        published_id = Fork.objects.get(id=fork_id).published_id
        print(published_id)
        save_video = SavedVideo.objects.get(published_id=published_id)
        print(save_video.id)
        video_details = get_video_details.get_video(str(save_video.id))
        return video_details


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
                    'published_at', 'duration'
                )),
                'saved_video': list(SavedVideo.objects.filter(user=user_pk).values(
                    'id', 'user__username', 'title', 'description', 'thumbnail', 'video_file',
                    'user__first_name', 'user__last_name',
                    'created_at', 'duration', 'is_published'
                )),

                'forked_video': list(Fork.objects.filter(user=user_pk).values(
                    'id', 'published_id__title', 'user__username', 'published_id__description',
                    'published_id__thumbnail',
                    'published_id__video_file',
                    'user__first_name', 'user__last_name',
                    'published_id__published_at', 'published_id__duration', 'published_id__is_paid'
                )),
            }

            return JsonResponse(videos)

# Do it through authenticated user.
