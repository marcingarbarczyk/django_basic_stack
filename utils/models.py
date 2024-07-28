from django.db import models
from django.utils import timezone

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
    activation_date = models.DateTimeField(null=True, blank=True)
    deactivation_date = models.DateTimeField(null=True, blank=True)

    active_objects = ActiveManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.is_active:
            self.activation_date = timezone.now()
            self.deactivation_date = None
        else:
            self.deactivation_date = timezone.now()

        super(ActiveMixin, self).save(*args, **kwargs)


class TimestampMixin(models.Model):
    """
    An abstract base class model with creation and modification date and time
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
