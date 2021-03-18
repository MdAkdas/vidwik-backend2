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
    thumbnail_img = open(os.path.join(BASE_DIR, request.data["info"]["image"].replace(BASE_URL, "")), "rb")
    gif = open(os.path.join(BASE_DIR, request.data["gif"].replace(BASE_URL, "")), "rb")

    # info
    try:
        user_pk = User.objects.get(username=request.data["info"]["user"])
    except:
        return JsonResponse({'error': 'UserDoesNotExist'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    title = request.data["info"]["title"]
    description = request.data["info"]["description"]
    thumbnail = File(thumbnail_img, name=request.data["info"]["image"].split('/')[-1])
    duration = datetime.strptime(str(timedelta(seconds=int(request.data["info"]["duration"]))), "%H:%M:%S").time()
    language = request.data["info"]["language"]

    published_at = datetime.utcnow()

    video_file = File(video, name=request.data["video"].split('/')[-1])
    tags = request.data["tags"]

    gif = File(gif, name=request.data["gif"].split('/')[-1])
    # collaborate = request.data["collaborate"]
    is_published = bool(request.data["is_published"])
    is_paid = bool(request.data["is_paid"])

    data = {
        'user': user_pk.username,
        'title': title,
        'thumbnail': thumbnail,
        'gif': gif,
        'video_file': video_file,
        'publish_at': published_at,
        'description': description,
        'duration': duration,
        'is_published': is_published,
        'is_paid': is_paid

    }

    upload = PublishVideoSerializer(data=data)
    if upload.is_valid():
        saved_pub_vid = upload.save()
        video.close()
        thumbnail_img.close()
        gif.close()

        #tags to saved video
        # pub_video_details = PublishedVideo.objects.get(id=saved_pub_vid.id)
        #
        # for tag in request.data["tags"]:
        #     t = Tags.objects.get_or_create(tag_text=tag)
        #     t[0].videos.add(pub_video_details)

        return Response({"Message": "Video  Published", "id": saved_pub_vid.id, "status": status.HTTP_201_CREATED})

    else:
        print(upload.errors)
        video.close()
        thumbnail_img.close()
        gif.close()
        return Response({"Message": "Some Error Occurred", "status": status.HTTP_400_BAD_REQUEST})
