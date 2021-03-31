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


# delete the old object and create a new saved video object
def update_video(request):
    save_video_id = request.data["save_video_id"]

    video = open(os.path.join(BASE_DIR, request.data["video"].replace(BASE_URL, "")), "rb")

    try:
        user_pk = User.objects.get(id=request.data["user_id"])
    except:
        return JsonResponse({'Message': 'UserDoesNotExist', "status": status.HTTP_400_BAD_REQUEST})

    if request.data["published_id"] != None:
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
    save_video = SavedVideo.objects.get(id=save_video_id)
    save_video.title=title
    save_video.thumbnail=thumbnail
    save_video.music_lib=bg_music_pk
    save_video.gif=gif
    save_video.video_file=video_file
    save_video.created_at=created_at
    save_video.description=description
    save_video.duration=duration
    save_video.is_published=is_published
    save_video.is_paid=is_paid
    save_video.published_id=published_id
    save_video.language=language
    save_video.save()

    updated_saved_video_details = SavedVideo.objects.get(id=save_video.id)
    video.close()
    thumbnail_bin.close()
    gif_bin.close()

    # what if the updated tags dont have a previous tag.
    for tag in request.data["tags"]:
        obj, created = Tags.objects.get_or_create(tag_text=tag)
        updated_saved_video_details.tags.add(obj.id)

    # print("debug2")
    # removing the old scene
    all_old_scenes = Scenes.objects.filter(video=updated_saved_video_details)
    for scene in all_old_scenes:
        old_subtitle = Subtitle.objects.filter(scene=scene)
        old_media = Media.objects.filter(scene=scene)
        old_audio = Audio.objects.filter(scene=scene)
        old_subtitle.delete()
        old_media.delete()
        old_audio.delete()
        scene.delete()


    addScenesToVideoRes = addScenesToVideo(request.data["scenes"], updated_saved_video_details)

    # print("debug3")
    if addScenesToVideoRes["status"] == 201:
        return Response({"Message": "Video Updated Successfully.", "id": updated_saved_video_details.id,
                         "status": status.HTTP_201_CREATED})

    else:
        updated_saved_video_details.delete()
        return Response({"Message": addScenesToVideoRes["Message"], "status": status.HTTP_400_BAD_REQUEST})
