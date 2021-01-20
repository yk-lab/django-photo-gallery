from functools import cached_property
from typing import Any, Dict

import exifread
from django.db import models, transaction
from django.utils.dateparse import parse_datetime
from django_photo_gallery.photos.utils.gps_exif import (
    get_alt, get_dest_bearing_ref, get_dest_bearing_value,
    get_h_positioning_error, get_img_direction_ref, get_img_direction_value,
    get_lat_lon, get_speed)
from model_utils.models import TimeStampedModel, UUIDModel

from .device import Device
from .exif import Exif
from .photo_meta import PhotoMeta
from .place import Place


class Photo(UUIDModel, TimeStampedModel):
    file = models.ImageField(width_field='width', height_field='height')
    width = models.IntegerField()
    height = models.IntegerField()
    shooting_datetime = models.DateTimeField(
        verbose_name='撮影日時', blank=True, null=True)
    device = models.ForeignKey(
        Device,
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    meta = models.OneToOneField(
        PhotoMeta,
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    exif = models.OneToOneField(
        Exif,
        on_delete=models.CASCADE,
        blank=True,
        null=True)

    @cached_property
    def get_exif(self) -> Dict[str, Any]:
        with self.file.open('rb') as img_file:
            return exifread.process_file(img_file)

    def set_place_from_exif(self):
        exif = self.get_exif
        if exif.get('Image GPSInfo'):
            # TODO: iPad 基準で言うと 'GPS GPSDate' を無視しているが，保持する必要あるか確認
            place = Place()
            gps_coords = get_lat_lon(exif)
            if gps_coords:
                lat, lon = gps_coords
                place.lat = lat
                place.lon = lon

            place.alt = get_alt(exif)
            place.speed = get_speed(exif)
            place.img_dir = get_img_direction_value(exif)
            place.img_dir_ref = get_img_direction_ref(exif)
            place.dest_bear = get_dest_bearing_value(exif)
            place.dest_bear_ref = get_dest_bearing_ref(exif)
            place.h_positioning_error = get_h_positioning_error(exif)

            with transaction.atomic():
                place.save()
                self.place = place

    def set_shooting_datetime_from_exif(self):
        exif = self.get_exif
        shooting_datetime = (
            (dt_org := exif.get('EXIF DateTimeOriginal').values) and dt_org
            or exif.get('Image DateTime').values)

        if not shooting_datetime:
            return

        shooting_date, shooting_time = shooting_datetime.split()
        shooting_datetime_offset = (
            (org_offset := exif.get('EXIF OffsetTimeOriginal')) and org_offset
            or exif.get('EXIF OffsetTime', ''))
        shooting_dt_str = f'{shooting_date.replace(":", "-")} {shooting_time}'
        shooting_dt_offset_str = f'{shooting_dt_str}{shooting_datetime_offset}'
        shooting_dt = parse_datetime(shooting_dt_offset_str)
        if shooting_dt:
            self.shooting_datetime = shooting_dt

    def set_device_from_exif(self):
        exif = self.get_exif
        maker = exif.get('Image Make')
        model = exif.get('Image Model')

        with transaction.atomic():
            device, _ = Device.objects\
                .get_or_create(manufacturer=maker, model=model)
            self.device = device
