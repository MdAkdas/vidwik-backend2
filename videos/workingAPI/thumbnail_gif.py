from moviepy.editor import *

from vidwik.global_variable import BASE_DIR
from django.core.files import File


def to_thumbnail(video_url):
    clip = VideoFileClip(video_url)
    file_path = video_url.split(".")[0] + ".png"
    clip.save_frame(file_path, 0)
    return file_path

def to_gif(video_url):
    clip = VideoFileClip(video_url)
    clip = clip.subclip(0, 2)
    file_path = video_url.split(".")[0] + ".gif"
    # saving video clip as gif
    clip.write_gif(file_path)
    return file_path
