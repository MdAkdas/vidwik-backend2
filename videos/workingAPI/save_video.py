from vidwik.settings import BASE_URL
from videos.models import *
from musicLibrary.models import MusicLib
from django.core.files import File
import os
from django.http import JsonResponse
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from .serializer import SaveVideoSerializer
from .helper_functions import addScenesToVideo

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def save(request):
    video = open(os.path.join(BASE_DIR, request.data["video"].replace(BASE_URL, "")), "rb")
    thumbnail_img = open(os.path.join(BASE_DIR, request.data["thumbnail"].replace(BASE_URL, "")), "rb")
    gif = open(os.path.join(BASE_DIR, request.data["gif"].replace(BASE_URL, "")), "rb")

    try:
        user_pk = User.objects.get(username=request.data["user"])
    except:
        return JsonResponse({'Message': 'UserDoesNotExist',"status":status.HTTP_400_BAD_REQUEST})

    try:
        published_video_pk = PublishedVideo.objects.get(id=request.data["published_video"])
    except:
        return JsonResponse({'Message': 'Published video doest not exist.',"status":status.HTTP_400_BAD_REQUEST})

    title = request.data["title"]
    description = request.data["description"]
    thumbnail = File(thumbnail_img, name=request.data["thumbnail"].split('/')[-1])
    duration = datetime.strptime(str(timedelta(seconds=int(request.data["duration"]))), "%H:%M:%S").time()
    language = request.data["language"]

    created_at = datetime.utcnow()

    video_file = File(video, name=request.data["video"].split('/')[-1])
    gif_file = File(gif, name=request.data["gif"].split('/')[-1])
    is_published = bool(request.data["is_published"])
    is_paid = bool(request.data["is_paid"])

    bg_music_pk = MusicLib.objects.get(title=request.data["bg_music"])

    print(published_video_pk.id)
    data = {
        'user': user_pk,
        'title': title,
        'thumbnail': thumbnail,
        'music_lib': bg_music_pk,
        'gif': gif_file,
        'video_file': video_file,
        'created_at': created_at,
        'description': description,
        'duration': duration,
        'is_published': is_published,
        'is_paid': is_paid,
        'published_video': published_video_pk
    }

    saved_video_details = SavedVideo.objects.create(**data)

    video.close()
    thumbnail_img.close()
    gif.close()

    for tag in request.data["tags"]:
        obj, created = Tags.objects.get_or_create(tag_text=tag)
        saved_video_details.tags.add(obj.id)

    # print("debug2")
    addScenesToVideoRes = addScenesToVideo(request.data["scenes"], saved_video_details)

    # print("debug3")
    if addScenesToVideoRes["status"] == 201:
        return Response({"Message": "Video Saved Successfully.", "id": saved_video_details.id,
                         "status": status.HTTP_201_CREATED})

    else:
        saved_video_details.delete()
        return Response({"Message": addScenesToVideoRes["Message"], "status": status.HTTP_400_BAD_REQUEST})
