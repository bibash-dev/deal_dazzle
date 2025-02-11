from django.db import models
from django.core.validators import MinValueValidator


class Order(models.Model):
    """
    Represents an order made by a customer.
    """
    first_name = models.CharField(
        max_length=50,
        verbose_name='First Name'
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Last Name'
    )
    email = models.EmailField(
        verbose_name='Email Address'
    )
    address = models.CharField(
        max_length=250,
        verbose_name='Address'
    )
    postal_code = models.CharField(
        max_length=20,
        verbose_name='Postal Code'
    )
    city = models.CharField(
        max_length=100,
        verbose_name='City'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )
    paid = models.BooleanField(
        default=False,
        verbose_name='Paid'
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'Order {self.id}'

    def __repr__(self):
        return f'<Order id={self.id}, paid={self.paid}, total_cost={self.get_total_cost()}>'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """
    Represents an item within an order.
    """
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name='Order'
    )
    product = models.ForeignKey(
        'store.Product',
        related_name='order_items',
        on_delete=models.CASCADE,
        verbose_name='Product'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Price',
        validators=[MinValueValidator(0)]
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Quantity',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f'OrderItem {self.id} (Order {self.order.id})'

    def __repr__(self):
        return f'<OrderItem id={self.id}, product={self.product.name}, quantity={self.quantity}, cost={self.get_cost()}>'

    def get_cost(self):
        return self.price * self.quantity
