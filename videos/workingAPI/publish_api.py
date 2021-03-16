from vidwik.settings import BASE_URL
from videos.models import PublishedVideo
from django.core.files import File
import os
from django.http import JsonResponse
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from .serializer import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def addMediaDetails(media_details_data):
    pass


def publish(request):
    video = open(os.path.join(BASE_DIR, request.data["video"].replace(BASE_URL, "")), "rb")
    thumbnail_img = open(os.path.join(BASE_DIR, request.data["info"]["image"].replace(BASE_URL, "")), "rb")
    gif = open(os.path.join(BASE_DIR, request.data["gif"].replace(BASE_URL, "")), "rb")

    print("pb 23")
    # info
    try:
        user_pk = User.objects.get(username=request.data["info"]["user"])
    except:
        return JsonResponse({'error': 'UserDoesNotExist'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    print(user_pk.username)
    title = request.data["info"]["title"]
    description = request.data["info"]["description"]
    thumbnail = File(thumbnail_img, name=request.data["info"]["image"].split('/')[-1])
    script = request.data["info"]["script"]
    url = request.data["info"]["url"]
    duration = datetime.strptime(str(timedelta(seconds=int(request.data["info"]["duration"]))), "%H:%M:%S").time(),
    language = request.data["info"]["language"]

    bgm = request.data["bgm"]
    id = request.data["id"]
    published_at = datetime.utcnow()

    # not required
    # is_save_later = request.data["is_save_later"]
    # scenes = request.data["scenes"]

    video_file = File(video, name=request.data["video"].split('/')[-1]),
    tags = request.data["tags"]

    # new field
    # media_details = MediaDetails.objects.get(id=request.data["media_details"]["id"])  # how to handle this
    # media_details_pk = addMediaDetails(media_details)

    gif = File(gif, name=request.data["gif"].split('/')[-1])
    # collaborate = request.data["collaborate"]
    is_published = bool(request.data["is_published"])
    is_paid = bool(request.data["is_paid"])

    data = {
        'user':user_pk.username,
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

    # upload = PublishVideoSerializer(PublishedVideo(user=user_pk), data=data)
    print(data)
    upload = PublishVideoSerializer(data=data)
    print(upload)
    if upload.is_valid():
        saved_pub_vid = upload.save()

        video.close()
        thumbnail_img.close()
        gif.close()

        pub_video_details = PublishedVideo.objects.get(id=saved_pub_vid.id)

        for tag in request.data["tags"]:
            t = Tags.objects.get_or_create(tag_text=tag)
            t[0].videos.add(pub_video_details)

        return Response({"Message": "Video  Published", "id": saved_pub_vid.id, "status": status.HTTP_201_CREATED})

    else:
        video.close()
        thumbnail_img.close()
        gif.close()
        return Response({"Message": "Some Error Occurred", "status": status.HTTP_400_BAD_REQUEST})

#
# PublishedVideo.objects.create(
#        user=user,
#        media_details=media_details,
#        title=title,
#        thumbnail=thumbnail,
#        gif=gif,
#        video_file=video_file,
#        published_at=published_at,
#        description=description,
#        duration=duration,
#        is_published=is_published,
#        is_paid=is_paid
#    )
