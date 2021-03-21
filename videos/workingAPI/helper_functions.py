from vidwik.settings import BASE_URL
from videos.models import *
from django.core.files import File
import os
from datetime import datetime, timedelta
from rest_framework import status
from .serializer import SceneSerializer, SubtitleSerializer, MediaSerializer, AudioSerializer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# subtitle OTO scene
def addSceneToSubtitle(subtitle, scene):
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
    # print(deserialized_subtitle)
    if deserialized_subtitle.is_valid():
        saved_subtitle = deserialized_subtitle.save()
        # saved_subtitle_detail = Subtitle.objects.get(id=saved_subtitle)
        # saved_subtitle_detail.scene.add(scene.id)
        return {"Message": "Subtitle added to scene", "status": status.HTTP_201_CREATED}

    else:
        # print(deserialized_subtitle.errors)
        return {"Message": deserialized_subtitle.errors, "status": status.HTTP_400_BAD_REQUEST}


# Media OTO scene
def addSceneToMedia(media, scene):
    item_duration = datetime.strptime(str(timedelta(seconds=int(media["item_duration"]))), "%H:%M:%S").time()
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
    # print(deserialized_media)
    if deserialized_media.is_valid():
        saved_media = deserialized_media.save()
        bin_med_file.close()
        # saved_media_detail = Subtitle.objects.get(id=saved_media)
        # saved_media_detail.scene.add(scene.id)
        return {"Message": "Media added to scene", "status": status.HTTP_201_CREATED}

    else:
        bin_med_file.close()
        # print(deserialized_media.errors)
        return {"Message": deserialized_media.errors, "status": status.HTTP_400_BAD_REQUEST}


# Audio OTO scene
def addSceneToAudio(audio, scene):
    bin_aud_file = open(os.path.join(BASE_DIR, audio["audio_file"].replace(BASE_URL, "")), "rb")
    audio_file = File(bin_aud_file, name=audio["audio_file"].split('/')[-1])
    # print(scene.id)
    audio_data = {
        "scene": scene.id,
        "audio_type": audio["audio_type"],
        "audio_file": audio_file
    }

    deserialized_audio = AudioSerializer(data=audio_data)
    # print(deserialized_audio)
    if deserialized_audio.is_valid():
        saved_media = deserialized_audio.save()
        bin_aud_file.close()
        return {"Message": "Audio added to scene", "status": status.HTTP_201_CREATED}

    else:
        bin_aud_file.close()
        # print(deserialized_audio.errors)
        return {"Message": deserialized_audio.errors, "status": status.HTTP_400_BAD_REQUEST}


# Scenes MTO to video
def addScenesToVideo(scenes, video):
    for i in scenes:
        scene_data = {
            "order": int(i),
            "title": scenes[i]["title"],
            "transition": "left_to_right",
            "video": video.id
        }
        # print("debug4")
        deserialized_scene = SceneSerializer(data=scene_data)
        # print("debug5")
        # print(deserialized_scene)
        if deserialized_scene.is_valid():
            saved_scene = deserialized_scene.save()
            # print("debug6")
            scenes_details = Scenes.objects.get(id=saved_scene.id)

            for tag in scenes[i]["keywords"]:
                obj, created = Tags.objects.get_or_create(tag_text=tag)
                scenes_details.tags.add(obj.id)

            # print("debug7")

            subtitle_response = addSceneToSubtitle(scenes[i]["subtitle"], scenes_details)
            # print("debug8")
            # print(subtitle_response)
            if subtitle_response["status"] != 201:
                scenes_details.delete()
                return subtitle_response

            # print("debug8.1")
            media_response = addSceneToMedia(scenes[i]["media"], scenes_details)
            # print("debug9")
            # print(media_response)
            if media_response["status"] != 201:
                scenes_details.delete()
                return media_response

            add_audio_response = addSceneToAudio(scenes[i]["audio"], scenes_details)
            # print("debug10")
            # print(add_audio_response)
            if add_audio_response["status"] != 201:
                scenes_details.delete()
                return add_audio_response

        else:
            # print(deserialized_scene.errors)
            return {"message": deserialized_scene.errors, "status": status.HTTP_400_BAD_REQUEST}

    return {"message": "Scenes Created!", "status": status.HTTP_201_CREATED}
