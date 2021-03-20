from vidwik.settings import BASE_URL
from videos.models import *
from musicLibrary.models import MusicLib
from django.core.files import File
import os
from django.http import JsonResponse
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from .serializer import SaveVideoSerializer, SceneSerializer,SubtitleSerializer, MediaSerializer, AudioSerializer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# subtitle OTO scene
def addSceneToSubtitle(subtitle,scene):
    subtitle_data = {
        "scene": scene.id,
        "alignment": subtitle["alignment"],
        "font_color": subtitle["font_color"],
        "background_color": subtitle["background_color"],
        "text_position": subtitle["text_position"],
        "text": subtitle["text"],
        "font_style": subtitle["font_style"],
        "font_size": subtitle["font_size"],
        "font_type": subtitle["font_type"],
    }

    deserialized_subtitle = SubtitleSerializer(data=subtitle_data)
    print(deserialized_subtitle)
    if deserialized_subtitle.is_valid():
        saved_subtitle = deserialized_subtitle.save()
        # saved_subtitle_detail = Subtitle.objects.get(id=saved_subtitle)
        # saved_subtitle_detail.scene.add(scene.id)
        return ({"Message": "Subtitle added to scene", "status": status.HTTP_201_CREATED})

    else:
        print(deserialized_subtitle.errors)
        return ({"Message": deserialized_subtitle.errors, "status": status.HTTP_400_BAD_REQUEST})

# Media OTO scene
def addSceneToMedia(media, scene):
    item_duration = datetime.strptime(str(timedelta(seconds=int(media["item_duration"]))),"%H:%M:%S").time()
    bin_med_file = open(os.path.join(BASE_DIR, media["media_file"].replace(BASE_URL, "")), "rb")
    media_file = File(bin_med_file, name=media["media_file"].split('/')[-1])

    media_data = {
        "scene": scene.id,
        "media_type": media["media_type"],
        "media_file": media_file,
        "item_duration": item_duration,
        "content_type": media["content_type"],
        "animation": media["animation"]
    }

    deserialized_media = MediaSerializer(data=media_data)
    print(deserialized_media)
    if deserialized_media.is_valid():
        saved_media = deserialized_media.save()
        bin_med_file.close()
        # saved_media_detail = Subtitle.objects.get(id=saved_media)
        # saved_media_detail.scene.add(scene.id)
        return ({"Message": "Media added to scene", "status": status.HTTP_201_CREATED})

    else:
        bin_med_file.close()
        print(deserialized_media.errors)
        return ({"Message": deserialized_media.errors, "status": status.HTTP_400_BAD_REQUEST})

# Audio OTO scene
def addSceneToAudio(audio,scene):
    bin_aud_file = open(os.path.join(BASE_DIR, audio["audio_file"].replace(BASE_URL, "")), "rb")
    audio_file = File(bin_aud_file, name=audio["audio_file"].split('/')[-1])
    print(scene.id)
    audio_data = {
        "scene": scene.id,
        "audio_type": audio["audio_type"],
        "audio_file": audio_file
    }

    deserialized_audio = AudioSerializer(data=audio_data)
    print(deserialized_audio)
    if deserialized_audio.is_valid():
        saved_media = deserialized_audio.save()
        bin_aud_file.close()
        return ({"Message": "Audio added to scene", "status": status.HTTP_201_CREATED})

    else:
        bin_aud_file.close()
        print(deserialized_audio.errors)
        return ({"Message": deserialized_audio.errors, "status": status.HTTP_400_BAD_REQUEST})


# Scenes MTO to video
def addScenesToVideo(scenes,video):

    for i in scenes:
        scene_data = {
            "order":int(i),
            "title":scenes[i]["title"],
            "transition":"left_to_right",
            "video":video.id
        }
        print("debug4")
        deserialised_scene = SceneSerializer(data=scene_data)
        print("debug5")
        print(deserialised_scene)
        if deserialised_scene.is_valid():
            saved_scene = deserialised_scene.save()
            print("debug6")
            scenes_details = Scenes.objects.get(id=saved_scene.id)

            for tag in scenes[i]["keywords"]:
                obj, created = Tags.objects.get_or_create(tag_text=tag)
                scenes_details.tags.add(obj.id)

            print("debug7")

            addSubtitleRes = addSceneToSubtitle(scenes[i]["subtitle"],scenes_details)
            print("debug8")
            print(addSubtitleRes)
            if(addSubtitleRes["status"]!=201):
                scenes_details.delete()
                return addSubtitleRes

            print("debug8.1")
            addSceneToMediaRes = addSceneToMedia(scenes[i]["media"],scenes_details)
            print("debug9")
            print(addSceneToMediaRes)
            if(addSceneToMediaRes["status"]!=201):
                scenes_details.delete()
                return addSceneToMediaRes

            addSceneToAudioRes = addSceneToAudio(scenes[i]["audio"], scenes_details)
            print("debug10")
            print(addSceneToAudioRes)
            if(addSceneToAudioRes["status"]!= 201):
                scenes_details.delete()
                return addSceneToAudioRes

        else:
            print(deserialised_scene.errors)
            return ({"message":deserialised_scene.errors, "status":status.HTTP_400_BAD_REQUEST})


    return ({"message": "Scenes Created!", "status": status.HTTP_201_CREATED})


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
    gif_file = File(gif, name=request.data["gif"].split('/')[-1])
    is_published = bool(request.data["is_published"])

    bg_music_pk = MusicLib.objects.get(title=request.data["bg_music"])
    print(bg_music_pk)
    data = {
        'user': user_pk.username,
        'title': title,
        'thumbnail': thumbnail,
        'music_lib': bg_music_pk,
        'gif': gif_file,
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

        saved_video_details = SavedVideo.objects.get(id=saved_vid.id)
        print("debug1")
        for tag in request.data["tags"]:
            obj, created = Tags.objects.get_or_create(tag_text=tag)
            saved_video_details.tags.add(obj.id)

        print("debug2")
        addScenesToVideoRes=addScenesToVideo(request.data["scenes"], saved_video_details)

        print("debug3")
        if addScenesToVideoRes["status"]==201:
            return Response({"Message": "Video Saved Successfully.", "id": saved_video_details.id, "status": status.HTTP_201_CREATED})

        else:
            saved_video_details.delete()
            return Response({"Message": addScenesToVideoRes["Message"], "status": status.HTTP_400_BAD_REQUEST})
    else:
        video.close()
        thumbnail_img.close()
        gif.close()
        return Response({"Message": upload.errors, "status": status.HTTP_400_BAD_REQUEST})
