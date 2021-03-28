# Generated by Django 3.1.7 on 2021-03-23 12:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0004_auto_20210320_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publishedvideo',
            name='gif',
            field=models.FileField(default=None, null=True, upload_to='publish/gifs/%Y/%m/%d/gif'),
        ),
        migrations.CreateModel(
            name='Fork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_video', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='videos.publishedvideo')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
