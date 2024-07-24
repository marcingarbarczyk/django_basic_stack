from django.db import models

from utils.managers import ActiveManager


class Orderable(models.Model):
    """
    An abstract class for models that are orderable.
    """

    order = models.IntegerField(
        default=0,
        verbose_name='kolejność',
    )

    class Meta:
        abstract = True
        ordering = ['order']


class ActiveMixin(models.Model):
    """
    An abstract base class model that can be active or not
    """

    is_active = models.BooleanField(default=True)
    active_objects = ActiveManager()

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    """
    An abstract base class model with creation and modification date and time
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
