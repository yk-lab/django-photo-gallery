from django.db import models
from model_utils.models import UUIDModel, TimeStampedModel


class PhotoMeta(UUIDModel, TimeStampedModel):
    aperture = models.DecimalField(
        verbose_name='絞り値', max_digits=3, decimal_places=1,
        blank=True, null=True)
    exposure_bias = models.IntegerField(verbose_name='', blank=True, null=True)
    exposure_mode = models.CharField(verbose_name='', max_length=16, blank=True)
    exposure_program = models.CharField(verbose_name='露出プログラム', max_length=16, blank=True)
    exposure_time = models.CharField(
        verbose_name='露出時間', max_length=16, blank=True)
    flash = models.BooleanField(blank=True, null=True)
    flash_mode = models.CharField(max_length=16, blank=True)
    f_number = models.DecimalField(
        verbose_name='絞り値', max_digits=3, decimal_places=1,
        blank=True, null=True)
    focal_length = models.DecimalField(
        verbose_name='レンズ焦点距離', max_digits=3, decimal_places=1,
        blank=True, null=True)
    iso_speed_ratings = models.IntegerField(blank=True, null=True)
    metering_mode = models.CharField(max_length=32, blank=True)
    shutter_speed = models.CharField(max_length=16, blank=True)
    white_blance = models.CharField(max_length=32, blank=True)
