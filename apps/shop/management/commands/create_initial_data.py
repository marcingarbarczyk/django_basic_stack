from django.core.management.base import BaseCommand
from apps.shop.factories import ProductFactory, CategoryFactory, OrderFactory, OrderItemFactory, UserFactory


class Command(BaseCommand):
    help = 'Create random users, products, categories, orders and order items'

    def handle(self, *args, **options):
        users = [UserFactory() for _ in range(5)]
        categories = [CategoryFactory() for _ in range(3)]
        products = [ProductFactory(category=categories[i % 3]) for i in range(10)]

        for user in users:
            order = OrderFactory(user=user)
            [OrderItemFactory(product=products[i % 10], order=order) for i in range(3)]

        self.stdout.write(self.style.SUCCESS('Data created successfully'))
