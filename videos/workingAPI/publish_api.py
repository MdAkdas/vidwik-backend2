from vidwik.settings import BASE_URL
from django.core.files import File
import os
from django.http import JsonResponse
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from .serializer import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def publish(request):
    video = open(os.path.join(BASE_DIR, request.data["video"].replace(BASE_URL, "")), "rb")
    thumbnail_img = open(os.path.join(BASE_DIR, request.data["thumbnail"].replace(BASE_URL, "")), "rb")
    gif = open(os.path.join(BASE_DIR, request.data["gif"].replace(BASE_URL, "")), "rb")

    # info
    try:
        user = User.objects.get(username=request.data["user"])
    except:
        return JsonResponse({'Message': 'UserDoesNotExist', "status": status.HTTP_400_BAD_REQUEST})
    title = request.data["title"]
    description = request.data["description"]
    thumbnail = File(thumbnail_img, name=request.data["thumbnail"].split('/')[-1])
    duration = datetime.strptime(str(timedelta(seconds=int(request.data["duration"]))), "%H:%M:%S").time()
    language = request.data["language"]

    published_at = datetime.utcnow()

    video_file = File(video, name=request.data["video"].split('/')[-1])

    gif = File(gif, name=request.data["gif"].split('/')[-1])
    is_published = bool(request.data["is_published"])
    is_paid = bool(request.data["is_paid"])

    print(user)
    print(user.pk)
    data = {
        'user': user,
        'title': title,
        'thumbnail': thumbnail,
        'gif': gif,
        'video_file': video_file,
        'published_at': published_at,
        'description': description,
        'duration': duration,
        'is_published': is_published,
        'is_paid': is_paid

    }

    pub_video_details = PublishedVideo.objects.create(**data)
    video.close()
    thumbnail_img.close()
    gif.close()

    for tag in request.data["tags"]:
        obj,created = Tags.objects.get_or_create(tag_text=tag)
        pub_video_details.tags.add(obj.id)

    return Response({"Message": "Video  Published", "id": pub_video_details.id, "status": status.HTTP_201_CREATED})
