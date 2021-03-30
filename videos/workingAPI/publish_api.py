from vidwik.settings import BASE_URL
from django.core.files import File
import os
from django.http import JsonResponse
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from .serializer import *
from .thumbnail_gif import to_thumbnail, to_gif

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def publish(request):
    video = open(os.path.join(BASE_DIR, request.data["video"].replace(BASE_URL, "")), "rb")

    # info
    try:
        user = User.objects.get(id=request.data["user_id"])
    except:
        return JsonResponse({'Message': 'UserDoesNotExist', "status": status.HTTP_400_BAD_REQUEST})

    title = request.data["title"]
    description = request.data["description"]
    duration = datetime.strptime(str(timedelta(seconds=int(request.data["duration"]))), "%H:%M:%S").time()
    language = request.data["language"]
    published_at = datetime.utcnow()

    video_file = File(video, name=request.data["video"].split('/')[-1])

    # thumbnail
    thumbnail_url = to_thumbnail(request.data["video"].replace(BASE_URL, ""))
    thumbnail_bin = open(os.path.join(BASE_DIR, thumbnail_url), "rb")
    thumbnail = File(thumbnail_bin, name=thumbnail_url.split('/')[-1])
    # gif
    gif_url = to_gif(request.data["video"].replace(BASE_URL, ""))
    gif_bin = open(os.path.join(BASE_DIR, gif_url), "rb")
    gif = File(gif_bin, name=gif_url.split('/')[-1])

    is_paid = bool(request.data["is_paid"])

    data = {
        'user': user,
        'title': title,
        'thumbnail': thumbnail,
        'gif': gif,
        'video_file': video_file,
        'published_at': published_at,
        'description': description,
        'duration': duration,
        'is_paid': is_paid,
        'language': language,
    }

    pub_video_details = PublishedVideo.objects.create(**data)
    video.close()
    thumbnail_bin.close()
    gif_bin.close()

    for tag in request.data["tags"]:
        obj, created = Tags.objects.get_or_create(tag_text=tag)
        pub_video_details.tags.add(obj.id)

    return Response({"Message": "Video  Published", "id": pub_video_details.id, "status": status.HTTP_201_CREATED})
