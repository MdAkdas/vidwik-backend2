# Generated by Django 3.1.7 on 2021-03-23 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0005_auto_20210323_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='audio_file',
            field=models.FileField(default=None, null=True, upload_to='saved/%Y/%m/%d/audio'),
        ),
        migrations.AlterField(
            model_name='publishedvideo',
            name='gif',
            field=models.FileField(default=None, null=True, upload_to='publish//%Y/%m/%d/gifs'),
        ),
        migrations.AlterField(
            model_name='publishedvideo',
            name='thumbnail',
            field=models.FileField(default=None, null=True, upload_to='publish/%Y/%m/%d/thumbnails'),
        ),
        migrations.AlterField(
            model_name='publishedvideo',
            name='video_file',
            field=models.FileField(default=None, null=True, upload_to='publish/%Y/%m/%d/videos'),
        ),
        migrations.AlterField(
            model_name='savedvideo',
            name='thumbnail',
            field=models.FileField(default=None, null=True, upload_to='saved/%Y/%m/%d/thumbnails'),
        ),
        migrations.AlterField(
            model_name='savedvideo',
            name='video_file',
            field=models.FileField(default=None, null=True, upload_to='saved/%Y/%m/%d/videos'),
        ),
    ]
