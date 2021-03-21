from moviepy.editor import *


def to_thumbnail(video_url):
    clip = VideoFileClip("example.mp4")
    clip.save_frame("thumbnail.jpg", t=1.00)


def to_gif(video_url):
    clip = VideoFileClip("dsa_geek.webm")
    # getting only first 3 seconds
    clip = clip.subclip(0, 3)
    # saving video clip as gif
    clip.write_gif("gfg_gif.gif")
