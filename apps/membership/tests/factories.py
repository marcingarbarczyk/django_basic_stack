from typing import Any, Optional

import factory

from apps.membership.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """
    Fabryka do tworzenia zwykłych użytkowników
    """

    email: str = factory.Faker('email')
    first_name: str = factory.Faker('first_name')
    last_name: str = factory.Faker('last_name')
    is_staff: bool = False

    class Meta:
        model: type = User

    @factory.post_generation
    def set_password(self: User, create: bool, extracted: Optional[str], **kwargs: Any) -> None:
        """
        Set a default or extracted password
        """
        password: str = extracted if extracted else 'password123'
        self.set_password(password)
        if create:
            self.save()


class StaffUserFactory(UserFactory):
    """
    Fabryka do tworzenia użytkowników w zespole
    """

    is_staff: bool = True
