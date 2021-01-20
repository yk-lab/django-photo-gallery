from django.contrib.gis.db import models
from model_utils.models import TimeStampedModel, UUIDModel


class Place(UUIDModel, TimeStampedModel):
    lon = models.DecimalField(max_digits=10, decimal_places=6)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    alt = models.FloatField(null=True)
    img_dir = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    img_dir_ref = models.CharField(max_length=2, blank=True, null=True)
    dest_bear = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    dest_bear_ref = models.CharField(max_length=2, blank=True, null=True)
    speed = models.FloatField(null=True)
    h_positioning_error = models.FloatField(null=True)
