# Generated by Django 3.1.7 on 2021-03-19 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musicLibrary', '0001_initial'),
        ('videos', '0002_auto_20210318_1336'),
    ]

    operations = [
        migrations.RenameField(
            model_name='media',
            old_name='type',
            new_name='media_type',
        ),
        migrations.RenameField(
            model_name='savedvideo',
            old_name='published_video_details',
            new_name='published_video',
        ),
        migrations.RenameField(
            model_name='scenes',
            old_name='animation',
            new_name='transition',
        ),
        migrations.RemoveField(
            model_name='savedvideo',
            name='bg_musicfile',
        ),
        migrations.RemoveField(
            model_name='scenes',
            name='narration',
        ),
        migrations.AddField(
            model_name='media',
            name='animation',
            field=models.CharField(choices=[('Zoom In', 'zoom in'), ('Zoom Out', 'zoom out')], max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='media',
            name='content_type',
            field=models.CharField(choices=[('Video', 'video'), ('Image', 'image')], default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='savedvideo',
            name='music_lib',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='musicLibrary.musiclib'),
        ),
        migrations.AlterField(
            model_name='media',
            name='media_file',
            field=models.FileField(blank=True, null=True, upload_to='scenes/media/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='savedvideo',
            name='gif',
            field=models.FileField(default=None, null=True, upload_to='saved/%Y/%m/%d/gifs'),
        ),
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_type', models.CharField(choices=[('Upload', 'upload'), ('Narration', 'narration')], max_length=20)),
                ('audio_file', models.FileField(default=None, null=True, upload_to='saved/audio/%Y/%m/%d/video')),
                ('scene', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='videos.savedvideo')),
            ],
        ),
    ]