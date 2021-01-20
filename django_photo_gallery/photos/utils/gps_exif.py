from typing import Any, Dict, Optional, Tuple
from exifread.utils import get_gps_coords


def get_lat_lon(exif: Dict[str, Any]) -> Optional[Tuple[float, float]]:
    return get_gps_coords(exif)


def get_lat(exif: Dict[str, Any]) -> Optional[float]:
    lat = None
    if lat_lon := get_lat_lon(exif):
        lat, _ = lat_lon
    return lat


def get_lon(exif: Dict[str, Any]) -> Optional[float]:
    lon = None
    if lat_lon := get_lat_lon(exif):
        _, lon = lat_lon
    return lon


def get_alt(exif: Dict[str, Any]) -> Optional[float]:
    if _alt := exif.get('GPS GPSAltitude'):
        if ref := exif.get('GPS GPSAltitudeRef'):
            alt = _alt.decimal() * (-1)**ref.values[0]
            return alt
    return None


def get_speed(exif: Dict[str, Any]) -> Optional[float]:
    if _speed := exif.get('GPS GPSSpeed'):
        if ref := exif.get('GPS GPSSpeedRef'):
            if ref.values == 'M':
                speed = _speed / 0.62137119223733
            elif ref.values == 'N':
                speed = _speed / 0.53995680345572
            elif ref.values == 'K':
                speed = _speed
            else:
                # TODO: logger に書き出したい
                speed = None
            if speed:
                return speed
    return None


def get_img_direction_value(exif: Dict[str, Any]) -> Optional[float]:
    if _dire := exif.get('GPS GPSImgDirection'):
        dire = [d.decimal() for d in _dire]
        if dire:
            return dire[0]
    return None


def get_dest_bearing_value(exif: Dict[str, Any]) -> Optional[float]:
    if _bear := exif.get('GPS GPSDestBearing'):
        bear = [d.decimal() for d in _bear]
        if bear:
            return bear[0]
    return None


def get_img_direction_ref(exif: Dict[str, Any]) -> Optional[str]:
    if ref := exif.get('GPS GPSImgDirectionRef'):
        if ref.values:
            return ref.values
    return None


def get_dest_bearing_ref(exif: Dict[str, Any]) -> Optional[str]:
    if ref := exif.get('GPS GPSDestBearingRef'):
        if ref.values:
            return ref.values
    return None


def get_h_positioning_error(exif: Dict[str, Any]) -> Optional[str]:
    if (_hpe := exif.get('GPS GPSHPositioningError'))\
            or (_hpe := exif.get('GPS Tag 0x001F')):
        # exifread が GPSHPositioningError 未対応なため 0x001F での取得を行う
        # 将来対応した時に備え事前に名称での取得を試みる
        hpe = [h.decimal() for h in _hpe]
        if hpe:
            return hpe[0]
    return None
