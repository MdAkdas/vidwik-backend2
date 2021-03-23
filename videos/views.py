from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from videos.models import PublishedVideo
from .workingAPI import publish_api, get_video_details, save_video
from .send_mail import sendMail
from .models import PublishedVideo

class PublishVideo(APIView):
    def post(self, request):
        return publish_api.publish(request)


class SaveLater(APIView):
    def post(self, request):
        return save_video.save(request)


class GetSavedVideo(APIView):
    def get(self, request):
        id = request.GET.get("id")
        print(id)
        return get_video_details.get_video(id)

class ForkVideo(APIView):
    def get(self, request):
        user = request.GET.get("user")
        published_video = request.GET.get("published_video")
        publish_video_details = PublishedVideo.objects.get(id=published_video)
        #todo create a new object with new user and save
        publish_video_details.user=user
        publish_video_details.id=None
        publish_video_details.save()