from django.contrib.gis.db import models
from model_utils.models import TimeStampedModel, UUIDModel


class Place(UUIDModel, TimeStampedModel):
    lon = models.FloatField()
    lat = models.FloatField()
    alt = models.FloatField(null=True)
