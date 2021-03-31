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
from .thumbnail_gif import to_thumbnail, to_gif

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def save(request):
    video = open(os.path.join(BASE_DIR, request.data["video"].replace(BASE_URL, "")), "rb")

    try:
        user_pk = User.objects.get(id=request.data["user_id"])
    except:
        return JsonResponse({'Message': 'UserDoesNotExist',"status":status.HTTP_400_BAD_REQUEST})

    if request.data["published_id"]!=None:
        published_id = PublishedVideo.objects.get(id=request.data["published_id"])
    else:
        published_id = request.data["published_id"]

    title = request.data["title"]
    description = request.data["description"]
    duration = datetime.strptime(str(timedelta(seconds=int(request.data["duration"]))), "%H:%M:%S").time()
    language = request.data["language"]

    # thumbnail
    thumbnail_url = to_thumbnail(request.data["video"].replace(BASE_URL, ""))
    thumbnail_bin = open(os.path.join(BASE_DIR, thumbnail_url), "rb")
    thumbnail = File(thumbnail_bin, name=thumbnail_url.split('/')[-1])
    # gif
    gif_url = to_gif(request.data["video"].replace(BASE_URL, ""))
    gif_bin = open(os.path.join(BASE_DIR, gif_url), "rb")
    gif = File(gif_bin, name=gif_url.split('/')[-1])
    created_at = datetime.utcnow()

    video_file = File(video, name=request.data["video"].split('/')[-1])
    is_published = bool(request.data["is_published"])
    is_paid = bool(request.data["is_paid"])

    bg_music_pk = MusicLib.objects.get(id=request.data["bg_music_id"])

    print(published_id)
    data = {
        'user': user_pk,
        'title': title,
        'thumbnail': thumbnail,
        'music_lib': bg_music_pk,
        'gif': gif,
        'video_file': video_file,
        'created_at': created_at,
        'description': description,
        'duration': duration,
        'is_published': is_published,
        'is_paid': is_paid,
        'published_id': published_id,
        'language': language
    }
    print(data)
    saved_video_details = SavedVideo.objects.create(**data)
    print("saved_video_details", saved_video_details)
    video.close()
    thumbnail_bin.close()
    gif_bin.close()

    for tag in request.data["tags"]:
        obj, created = Tags.objects.get_or_create(tag_text=tag)
        saved_video_details.tags.add(obj.id)

    # print("debug2")
    addScenesToVideoRes = addScenesToVideo(request.data["scenes"], saved_video_details)
    print("addScenesToVideoRes",addScenesToVideoRes)
    # print("debug3")
    if addScenesToVideoRes["status"] == 201:
        return {"Message": "Video Saved Successfully.", "id": saved_video_details.id,
                         "status": status.HTTP_201_CREATED}

    else:
        saved_video_details.delete()
        return {"Message": addScenesToVideoRes["Message"], "status": status.HTTP_400_BAD_REQUEST}
