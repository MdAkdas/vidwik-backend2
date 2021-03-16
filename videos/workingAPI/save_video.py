from vidwik.settings import BASE_URL
from videos.models import *
from django.core.files import File
import os
from django.http import JsonResponse
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from .serializer import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def save(request):
    try:
        user = User.objects.get(username=request.data["user"]["username"])
    except:
        return JsonResponse({'error': 'UserDoesNotExist'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    media_details = MediaDetails.objects.get(id=request.data["media_details"]["id"])

    # media_library
    # published_video
    video = open(os.path.join(BASE_DIR, request.data["video_file"].replace(BASE_URL, "")), "rb")
    gif = open(os.path.join(BASE_DIR, request.data["gif"].replace(BASE_URL, "")), "rb")
    thumbnail_img = open(os.path.join(BASE_DIR, request.data["thumbnail"].replace(BASE_URL, "")), "rb")
    data = {
        'is_paid': bool(request.data["is_paid"]),
        'is_published': bool(request.data["is_published"]),
        'title': request.data["title"],
        'thumbnail': File(thumbnail_img, name=request.data["thumbnail"].split('/')[-1]),
        'gif': File(gif, name=request.data["gif"].split('/')[-1]),
        'video_file': File(video, name=request.data["video_file"].split('/')[-1]),
        'created_at': datetime.utcnow(),
        'description': request.data["description"],
        'duration': datetime.strptime(str(timedelta(seconds=int(request.data["duration"]))), "%H:%M:%S").time(),
    }
    scenes = Scenes.objects.get(id=request.data["Scenes"]["id"])
    audio = Audio.objects.get(id=request.data["Audio"]["id"])

    upload = SaveVideoSerializer(SavedVideo(user=user, media_details=media_details, scenes=scenes, audio=audio),
                                 data=data)

    if upload.is_valid():
        saved_vid = upload.save()

        video.close()
        thumbnail_img.close()
        gif.close()

        save_video_details = PublishedVideo.objects.get(id=saved_vid.id)

        for tag in request.data["tags"]:
            t = Tags.objects.get_or_create(tag_text=tag)
            t[0].videos.add(save_video_details)

        return Response({"Message": "Video Saved", "id": save_video_details.id, "status": status.HTTP_201_CREATED})

    else:
        video.close()
        thumbnail_img.close()
        gif.close()
        return Response({"Message": "Some Error Occurred", "status": status.HTTP_400_BAD_REQUEST})
