from videos.models import *
from rest_framework.serializers import ModelSerializer


# class UserSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username')

class PublishVideoSerializer(ModelSerializer):
    # user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = PublishedVideo
        fields = '__all__'
        depth = 1


class SaveVideoSerializer(ModelSerializer):
    # user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = SavedVideo
        fields = '__all__'
        depth = 1

    # def to_representation(self, instance):
    #     self.fields['user'] = UserSerializer(read_only=True)
    #     return super(SaveVideoSerializer, self).to_representation(instance)

class SceneSerializer(ModelSerializer):
    class Meta:
        model = Scenes
        fields = '__all__'


class SubtitleSerializer(ModelSerializer):
    class Meta:
        model = Subtitle
        fields = '__all__'


class MediaSerializer(ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'


class AudioSerializer(ModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'
