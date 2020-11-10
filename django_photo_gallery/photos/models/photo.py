from django.db import models
from model_utils.models import UUIDModel


class Photo(UUIDModel):
    file = models.ImageField()
