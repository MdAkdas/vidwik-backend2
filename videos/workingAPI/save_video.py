from vidwik.settings import BASE_URL
from videos.models import *
from django.core.files import File
import os
from django.http import JsonResponse
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from .serializer import SaveVideoSerializer, SceneSerializer,SubtitleSerializer, MediaSerializer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def addScenes(scenes,video):

    for i in scenes:
        scene_data = {
            "order":int(i),
            "title":scenes[i]["title"],
            "video":video.id
        }

        deserialised_scene = SceneSerializer(data=scene_data)

        if deserialised_scene.is_valid():
            saved_scene = deserialised_scene.save()
            scenes_details = Scenes.objects.get(id=saved_scene.id)

            subtitle_data = {
                "scene":scenes_details.id,
                "alignment": scenes[i]["subtitle"]["alignment"],
                "font_color": scenes[i]["subtitle"]["font_color"],
                "background_color": scenes[i]["subtitle"]["background_color"],
                "text_position": scenes[i]["subtitle"]["text_position"],
                "text": scenes[i]["subtitle"]["text"],
                "font_style": scenes[i]["subtitle"]["font_style"],
                "font_size": scenes[i]["subtitle"]["font_size"],
                "font_type": scenes[i]["subtitle"]["font_type"],
            }

            deserialized_subtitle = SubtitleSerializer(data=subtitle_data)

            if deserialized_subtitle.is_valid():
                saved_subtitle = deserialized_subtitle.save()

            else:
                return Response(deserialized_subtitle.errors, status=status.HTTP_400_BAD_REQUEST)
            item_duration = datetime.strptime(str(timedelta(seconds=int(scenes[i]["media"]["item_duration"]))), "%H:%M:%S").time()
            media_data = {
                "scene": scenes_details.id,
                "type": scenes[i]["media"]["type"],
                "media_file": scenes[i]["media"]["media_file"],
                "item_duration": scenes[i]["media"]["item_duration"],
            }

            deserialized_media =MediaSerializer(data=media_data)

            if deserialized_media.is_valid():
                saved_media = deserialized_media.save()

            else:
                return Response(deserialized_media.errors, status=status.HTTP_400_BAD_REQUEST)

            for tag in scenes["keywords"]:
                obj, created = Tags.objects.get_or_create(tag_text=tag)
                scenes_details.tags.add(obj.id)


            return Response(status.HTTP_200_OK)

        else:
            return Response(deserialised_scene.errors, status=status.HTTP_400_BAD_REQUEST)


def save(request):
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

    created_at = datetime.utcnow()

    video_file = File(video, name=request.data["video"].split('/')[-1])
    tags = request.data["tags"]

    gif = File(gif, name=request.data["gif"].split('/')[-1])
    # collaborate = request.data["collaborate"]
    is_published = bool(request.data["is_published"])

    data = {
        'user': user_pk.username,
        'title': title,
        'thumbnail': thumbnail,
        'gif': gif,
        'video_file': video_file,
        'created_at': created_at,
        'description': description,
        'duration': duration,
        'is_published': is_published,
    }

    upload = SaveVideoSerializer(data=data)

    if upload.is_valid():
        saved_vid = upload.save()
        video.close()
        thumbnail_img.close()
        gif.close()

        save_video_details = SavedVideo.objects.get(id=saved_vid.id)
        for tag in request.data["tags"]:
            obj, created = Tags.objects.get_or_create(tag_text=tag)
            save_video_details.tags.add(obj.id)

        resp=addScenes(request.data["scenes"], save_video_details)

        if resp.status_code==200:
            return Response({"Message": "Video Saved", "id": save_video_details.id, "status": status.HTTP_201_CREATED})

        else:
            return Response({"Message": "Some Error Occurred", "status": status.HTTP_400_BAD_REQUEST})

    else:
        video.close()
        thumbnail_img.close()
        gif.close()
        return Response({"Message": "Some Error Occurred", "status": status.HTTP_400_BAD_REQUEST})
