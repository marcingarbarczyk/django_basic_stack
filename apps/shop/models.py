from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _


class Product(models.Model):
    """
    This represents a single product available for purchase.
    Each product has a name, description, price, and is associated with a category.
    """

    name = models.CharField(
        max_length=255,
        verbose_name=_('name'),
    )
    description = models.TextField(
        verbose_name=_('description'),
    )
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name=_('price'),
    )
    category = models.ForeignKey(
        'Category',
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name=_('category'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')


class Category(models.Model):
    """
    This represents a category to which products are associated.
    Each category has a name and description.
    """

    name = models.CharField(
        max_length=255,
        verbose_name=_('name'),
    )
    description = models.TextField(
        verbose_name=_('description'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class Order(models.Model):
    """
    This represents an order placed by a user.
    Each order is associated with a user and has a date when it was ordered.
    """

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name=_('user'),
    )
    date_ordered = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('date ordered'),
    )

    def __str__(self):
        return f'Order {self.id}'

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')


class OrderItem(models.Model):
    """
    This represents an item within an order.
    Each item is associated with a product and an order, and has a quantity.
    """

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        verbose_name=_('product'),
    )
    order = models.ForeignKey(
        'Order',
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name=_('order'),
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_('quantity'),
    )

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'

    class Meta:
        verbose_name = _('order item')
        verbose_name_plural = _('order items')
