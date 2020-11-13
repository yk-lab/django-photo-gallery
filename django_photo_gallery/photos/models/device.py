from typing import List
from model_utils.models import UUIDModel, TimeStampedModel
from django.db import models


class Device(UUIDModel, TimeStampedModel):
    class Meta:
        unique_together = [['manufacturer', 'model']]

    manufacturer = models.CharField(verbose_name='カメラの製造元', max_length=255)
    model = models.CharField(verbose_name='カメラのモデル', max_length=255)
