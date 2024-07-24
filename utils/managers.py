from django.db import models


class ActiveManager(models.Manager):
    """
    A manager that allows you to filter the queryset by an active model
    """

    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)
