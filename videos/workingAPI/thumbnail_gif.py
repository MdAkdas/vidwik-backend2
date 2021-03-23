from moviepy.editor import *

from vidwik.global_variable import BASE_DIR
from django.core.files import File


def to_thumbnail(video_url):
    clip = VideoFileClip(video_url)
    imgpath = video_url.split(".")[0] + ".png"
    clip.save_frame(imgpath, 0)
    return imgpath

def to_gif(video_url):
    clip = clip.subclip(0, 3)
    # saving video clip as gif
    clip.write_gif("gfg_gif.gif")
