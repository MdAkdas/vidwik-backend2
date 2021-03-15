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


def publish(request):
    try:
        user = User.objects.get(username=request.data["user"]["username"])
    except:
        return JsonResponse({'error': 'UserDoesNotExist'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    media_details = MediaDetails.objects.get(id=request.data["media_details"]["id"])

    # collaborate = request.data["collaborate"]
    video = open(os.path.join(BASE_DIR, request.data["video_file"].replace(BASE_URL, "")), "rb")
    gif = open(os.path.join(BASE_DIR, request.data["gif"].replace(BASE_URL, "")), "rb")
    thumbnail_img = open(os.path.join(BASE_DIR, request.data["thumbnail"].replace(BASE_URL, "")), "rb"),
    data = {
        'title': request.data["title"],
        'thumbnail': File(thumbnail_img, name=request.data["thumbnail"].split('/')[-1]),
        'gif': File(gif, name=request.data["gif"].split('/')[-1]),
        'video_file': File(video, name=request.data["video_file"].split('/')[-1]),
        'published_at': datetime.utcnow(),
        'description': request.data["description"],
        'duration': datetime.strptime(str(timedelta(seconds=int(request.data["duration"]))),"%H:%M:%S").time(),
        'is_published': bool(request.data["is_published"]),
        'is_paid': bool(request.data["is_paid"]),
    }

    upload = VideoSerializer(PublishedVideo(user=user, media_details=media_details), data=data)

    if upload.is_valid():
        saved_pub_vid = upload.save()

        video.close()
        thumbnail_img.close()
        gif.close()

        pub_video_details=PublishedVideo.objects.get(id=saved_pub_vid.id)

        for tag in request.data["tags"]:
            t=Tags.objects.get_or_create(tag=tag)
            t[0].videos.add(pub_video_details)

        return Response({"Message": "Video  Published", "id" : saved_pub_vid.id, "status":status.HTTP_201_CREATED})

    else:
        video.close()
        thumbnail_img.close()
        gif.close()
        return Response({"Message": "Some Error Occurred", "status":status.HTTP_400_BAD_REQUEST})


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
