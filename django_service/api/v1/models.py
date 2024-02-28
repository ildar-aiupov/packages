import uuid

from django.db import models
from django.core.validators import MinValueValidator

from .validators import name_validator


class PackageType(models.Model):
    """Модель типа посылки."""

    name = models.CharField(max_length=200, blank=False, unique=True, verbose_name="Название типа")

    class Meta:
        verbose_name = "Тип посылки"
        verbose_name_plural = "Типы посылок"


class Package(models.Model):
    """Модель посылки."""

    uuid = models.CharField(primary_key=True, default=uuid.uuid4, max_length=60)
    name = models.CharField(max_length=200, blank=False, validators=[name_validator], verbose_name="Название пасылки")
    weight = models.FloatField(blank=False, validators=[MinValueValidator(0.001)], verbose_name="Вес")
    type = models.ForeignKey(
        PackageType, on_delete=models.DO_NOTHING, blank=False, to_field="name", verbose_name="Тип"
    )
    content_cost = models.FloatField(blank=False, validators=[MinValueValidator(0.0)], verbose_name="Стоимость содержимого")
    delivery_cost = models.FloatField(blank=False, validators=[MinValueValidator(0.0)], verbose_name="Стоимость доставки")
    sessionid = models.CharField(max_length=200, blank=False, verbose_name="Сессия")

    class Meta:
        verbose_name = "Посылка"
        verbose_name_plural = "Посылки"
