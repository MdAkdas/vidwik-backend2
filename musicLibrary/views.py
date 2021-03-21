from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MusicLib
from .serializer import MusicSerializer


class MusicList(APIView):
    def get(self, request):
        if request.GET.get("genre") == "all":
            music = MusicLib.objects.all().order_by("title")
            musicserializer = MusicSerializer(music, many=True)
            return Response({'data': musicserializer.data}, status=status.HTTP_200_OK)
        else:
            music = MusicLib.objects.filter(genre=request.GET.get("genre")).order_by("title")
            musicserializer = MusicSerializer(music, many=True)
            return Response({'data': musicserializer.data}, status=status.HTTP_200_OK)
