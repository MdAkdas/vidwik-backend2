from videos.models import *
from rest_framework.response import Response
from rest_framework import status
from vidwik.settings import BASE_URL
import os


def get_video(id):
    try:
        saved_video_details = SavedVideo.objects.get(id=int(id))
        data = {
            "id": saved_video_details.id,
            "user": saved_video_details.user,
            "title": saved_video_details.title,
            "description": saved_video_details.title,
            "thumbnail": os.path.join(BASE_URL, saved_video_details.thumbnail.url[1:]),
            "duration": saved_video_details.duration,
            "video": os.path.join(BASE_URL, saved_video_details.video_file.url[1:]),
            "bg_music": saved_video_details.music_lib,
            "gif": os.path.join(BASE_URL, saved_video_details.gif.url[1:]),
            "is_published": saved_video_details.is_published,
            "is_paid": saved_video_details.is_paid,
            "scenes": {

            },
            "tags": []
        }

        # scene -> subtitle and media
        all_scenes = Scenes.objects.filter(video=saved_video_details)
        # print("before all scene")
        for scene in all_scenes:
            data["scenes"][str(scene.order)] = {
                "title": scene.title,
                "transition": scene.transition,
                "subtitle": {

                },
                "media": {

                },
                "audio": {

                },
                "keywords": []
            }
            # print(data)
            # print("before subtitle")
            subtitle_info = Subtitle.objects.get(scene=scene)

            data["scenes"][str(scene.order)]["subtitle"] = {
                "alignment": subtitle_info.alignment,
                "font_color": subtitle_info.font_color,
                "background_color": subtitle_info.font_color,
                "text_position": subtitle_info.text_position,
                "text": subtitle_info.text,
                "font_style": subtitle_info.font_style,
                "font_size": subtitle_info.font_size,
                "font_type": subtitle_info.font_type
            }

            # print("before Media")
            media_info = Media.objects.get(scene=scene)

            data["scenes"][str(scene.order)]["media"] = {
                "media_type": media_info.media_type,
                "media_file": os.path.join(BASE_URL,media_info.media_file.url[1:]),
                "item_duration": media_info.item_duration,
                "content_type": media_info.content_type,
                "animation": media_info.animation,
            }
            # print(data)
            # print("before Audio")
            audio_info = Audio.objects.get(scene=scene)
            data["scenes"][str(scene.order)]["audio"] = {
                "audio_type": audio_info.audio_type,
                "audio_file": os.path.join(BASE_URL,audio_info.audio_file.url[1:])
            }
            # print(data)

            data["scenes"][str(scene.order)]["keywords"] = []
            for tags in scene.tags.all():
                data["scenes"][str(scene.order)]["keywords"].append(tags.tag_text)
            # print(data)

        for tags in saved_video_details.tags.all():
            data["tags"].append(tags.tag_text)

        # print(data)
        return Response(data, status.HTTP_200_OK)

    except SavedVideo.DoesNotExist:
        return Response({"Message": "Video doesn't exist", "status":status.HTTP_404_NOT_FOUND})

