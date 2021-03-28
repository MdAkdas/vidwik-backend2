from vidwik.settings import BASE_URL, BASE_DIR
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

# todo need whole flow
# todo pre_save signal
def update_video(request):

        save_video_id = request.data["save_video_id"]

        video = open(os.path.join(BASE_DIR, request.data["video"].replace(BASE_URL, "")), "rb")
        gif = open(os.path.join(BASE_DIR, request.data["gif"].replace(BASE_URL, "")), "rb")

        try:
            user_pk = User.objects.get(username=request.data["user"])
        except:
            return JsonResponse({'Message': 'UserDoesNotExist', "status": status.HTTP_400_BAD_REQUEST})

        if request.data["published_video"] != None:
            published_video_pk = PublishedVideo.objects.get(id=request.data["published_video"])
        else:
            published_video_pk = request.data["published_video"]

        title = request.data["title"]
        description = request.data["description"]
        duration = datetime.strptime(str(timedelta(seconds=int(request.data["duration"]))), "%H:%M:%S").time()
        language = request.data["language"]

        # thumbnail
        thumbnail_url = to_thumbnail(request.data["video"].replace(BASE_URL, ""))
        thumbnail_bin = open(os.path.join(BASE_DIR, thumbnail_url), "rb")
        thumbnail = File(thumbnail_bin, name=thumbnail_url.split('/')[-1])

        created_at = datetime.utcnow()

        video_file = File(video, name=request.data["video"].split('/')[-1])
        gif_file = File(gif, name=request.data["gif"].split('/')[-1])
        is_published = bool(request.data["is_published"])
        is_paid = bool(request.data["is_paid"])

        bg_music_pk = MusicLib.objects.get(title=request.data["bg_music"])

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
        updated_saved_video_details = SavedVideo.objects.update(**data)

        video.close()
        thumbnail_bin.close()
        gif.close()

        for tag in request.data["tags"]:
            obj, created = Tags.objects.get_or_create(tag_text=tag)
            updated_saved_video_details.tags.add(obj.id)

        # print("debug2")
        addScenesToVideoRes = addScenesToVideo(request.data["scenes"], updated_saved_video_details)

        # print("debug3")
        if addScenesToVideoRes["status"] == 201:
            return Response({"Message": "Video Saved Successfully.", "id": updated_saved_video_details.id,
                             "status": status.HTTP_201_CREATED})

        else:
            updated_saved_video_details.delete()
            return Response({"Message": addScenesToVideoRes["Message"], "status": status.HTTP_400_BAD_REQUEST})
