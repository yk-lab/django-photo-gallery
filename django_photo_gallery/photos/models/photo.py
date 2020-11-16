from django.db import models
from model_utils.models import TimeStampedModel, UUIDModel

from .device import Device
from .place import Place
from .photo_meta import PhotoMeta
from .exif import Exif


class Photo(UUIDModel, TimeStampedModel):
    file = models.ImageField(width_field='width', height_field='height')
    width = models.IntegerField()
    height = models.IntegerField()
    shooting_datetime = models.DateTimeField(verbose_name='撮影日時', null=True)
    device = models.ForeignKey(Device, on_delete=models.PROTECT, null=True)
    place = models.OneToOneField(Place, on_delete=models.CASCADE, null=True)
    meta = models.OneToOneField(PhotoMeta, on_delete=models.CASCADE, null=True)
    exif = models.OneToOneField(Exif, on_delete=models.CASCADE, null=True)
