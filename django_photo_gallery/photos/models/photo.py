from django.db import models
from model_utils.models import TimeStampedModel, UUIDModel

from .device import Device


class Photo(UUIDModel, TimeStampedModel):
    file = models.ImageField()
    device = models.ForeignKey(Device, on_delete=models.PROTECT, null=True)
