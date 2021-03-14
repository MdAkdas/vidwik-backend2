from django.db import models
from videos.models import PublishedVideo

class BuyModel(models.Model):
    exchange_key=models.CharField(max_length=200,null=True)
    dod=models.CharField(max_length=200,null=True)
    dataToken=models.CharField(max_length=200,null=True)
    paid=models.BooleanField(default=True,null=True)
    video=models.ForeignKey(PublishedVideo,null=True,on_delete=models.CASCADE)

