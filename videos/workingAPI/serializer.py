from videos.models import *
from rest_framework.serializers import ModelSerializer


class PublishVideoSerializer(ModelSerializer):
    class Meta:
        model = PublishedVideo
        fields = '__all__'
        depth = 1

#
# class SaveVideoSerializer(ModelSerializer):
#     class Meta:
#         model = SavedVideo
#         fields = '__all__'
#         depth = 1
#
#
# class SceneSerializer(ModelSerializer):
#     class Meta:
#         model = Scenes
#         fields = '__all__'
#

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'
