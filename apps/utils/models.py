import uuid
from typing import Any, Type

from django.conf import settings
from django.db import models
from django.db.models import Model
from django.utils import timezone
from django.utils.text import slugify


class TimeStampMixin(models.Model):
    """
    Mixin dodający pola `created_at` i `updated_at` do modelu Django.
    - `created_at`: Rejestruje datę i godzinę utworzenia rekordu.
    - `updated_at`: Rejestruje datę i godzinę ostatniej aktualizacji rekordu.

    Mixin ten jest oznaczony jako abstrakcyjny.
    """

    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class ActiveMixin(models.Model):
    """
    Mixin dodający obsługę statusu aktywności modelu.
    - `is_active`: Określa, czy obiekt jest aktywny.
    - `activation_date`: Data aktywacji obiektu, ustawiana automatycznie, gdy obiekt jest aktywowany.
    - `deactivation_date`: Data dezaktywacji obiektu, ustawiana automatycznie, gdy obiekt jest dezaktywowany.

    Uwaga: Funkcja `save` automatycznie zarządza polami dat aktywacji
    i dezaktywacji w zależności od statusu `is_active`.

    Mixin ten jest oznaczony jako abstrakcyjny.
    """

    is_active: models.BooleanField = models.BooleanField(
        default=True,
    )
    activation_date: models.DateTimeField = models.DateTimeField(
        blank=True,
        null=True,
    )
    deactivation_date: models.DateTimeField = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.is_active:
            if not self.activation_date:
                self.activation_date = timezone.now()
            self.deactivation_date = None
        else:
            if self.pk:
                self.deactivation_date = timezone.now()
        super().save(*args, **kwargs)


class OrderableMixin(models.Model):
    """
    Mixin dodający możliwość porządkowania obiektów na podstawie pola `position`.
    - `position`: Pole liczbowe określające pozycję obiektu w ramach porządkowania.

    Modele wykorzystujące ten mixin są domyślnie sortowane według pola `position`.

    Mixin ten jest oznaczony jako abstrakcyjny.
    """

    position: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        abstract = True
        ordering = ['position']


class UUIDMixin(models.Model):
    """
    Mixin zapewniający wykorzystanie pola `id` jako unikalnego identyfikatora
    UUID dla każdego rekordu.
    - `id`: Definiuje unikalny identyfikator oparty na UUID,
    ustawiany automatycznie podczas tworzenia rekordu.

    Mixin ten jest oznaczony jako abstrakcyjny.
    """

    id: models.UUIDField = models.UUIDField(  # noqa VNE003
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class UserRequiredMixin(models.Model):
    """
    Mixin dodający odniesienie do użytkownika (`user`) wymaganego dla obiektu.
    - `user`: Pole klucza obcego odnoszące się do modelu użytkownika definiowanego
    przez `settings.AUTH_USER_MODEL`. Usunięcie użytkownika powoduje usunięcie obiektu.

    Mixin ten jest oznaczony jako abstrakcyjny.
    """

    user: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class UserNotRequiredMixin(models.Model):
    """
    Mixin dodający odniesienie do użytkownika (`user`), które może być opcjonalne.
    - `user`: Pole klucza obcego odnoszące się do modelu użytkownika definiowanego
    przez `settings.AUTH_USER_MODEL`. Wartość `null` jest dozwolona.
    W przypadku usunięcia użytkownika pole może zostać ustawione na `NULL`.

    Mixin ten jest oznaczony jako abstrakcyjny.
    """

    user: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    """
    Mixin dodający pole `slug` oraz logikę do generowania unikalnych slugów opartych na źródle.
    - `slug`: Unikalny, opcjonalny identyfikator tekstowy
    (generowany automatycznie na podstawie pola `SLUG_SOURCE_FIELD`).
    - `SLUG_SOURCE_FIELD`: Pole, którego zawartość służy jako podstawa do wygenerowania `slug`.
    - `SLUG_FIELD_MAX_LENGTH`: Maksymalna długość pola `slug`.

    Mechanizm generowania:
    - Jeżeli `slug` nie jest ustawione, generowany jest automatycznie na podstawie wartości
      pola określonego w `SLUG_SOURCE_FIELD`.
    - W przypadku konfliktu (istniejący `slug` w bazie danych),
      dodawany jest licznik tworzący unikalność `slug`.

    Mixin ten jest oznaczony jako abstrakcyjny.
    """

    slug: models.SlugField = models.SlugField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        verbose_name='slug',
    )

    SLUG_SOURCE_FIELD: str = 'name'
    SLUG_FIELD_MAX_LENGTH: int = 255

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            slug_source: str = getattr(self, self.SLUG_SOURCE_FIELD, '')
            self.slug = self.generate_unique_slug(slug_source)
        super().save(*args, **kwargs)

    def generate_unique_slug(self, source: str) -> str:
        base_slug: str = slugify(source)[: self.SLUG_FIELD_MAX_LENGTH]
        slug: str = base_slug
        model_class: Type[Model] = self.__class__
        counter: int = 1

        while model_class.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    class Meta:
        abstract = True
