from model_utils.models import TimeStampedModel, UUIDModel
from django.db import models


class Exif(UUIDModel, TimeStampedModel):
    exif = models.TextField(verbose_name='exifデータ', default='{}')
