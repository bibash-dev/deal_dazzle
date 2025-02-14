from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from decimal import Decimal
from coupons.models import Coupon


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
        verbose_name='Created At',
        db_index=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )
    paid = models.BooleanField(
        default=False,
        verbose_name='Paid',
        db_index=True
    )
    stripe_id = models.CharField(
        max_length=250,
        blank=True,
        verbose_name='Stripe ID'
    )
    coupon = models.ForeignKey(
        Coupon,
        related_name='orders',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Coupon'
    )
    discount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Discount (%)'
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['paid']),
        ]
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'Order {self.id}'

    def __repr__(self):
        return f'<Order id={self.id}, paid={self.paid}, total_cost={self.get_total_cost()}>'

    def get_total_cost_before_discount(self):
        """Calculate total cost before any discounts are applied."""
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        """Calculate the discount amount based on the percentage."""
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)

    def get_total_cost(self):
        """Calculate the final cost after applying any discount."""
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()

    def get_stripe_url(self):
        """Generate Stripe dashboard URL for this payment."""
        if not self.stripe_id:
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            environment_path = '/test/'
        else:
            environment_path = '/'
        return f'https://dashboard.stripe.com{environment_path}payments/{self.stripe_id}'

    def get_absolute_url(self):
        """Get URL for viewing a particular order."""
        return reverse('orders:order_detail', args=[self.id])


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
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Quantity',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product']),
        ]

    def __str__(self):
        return f'{self.quantity}x {self.product.name} in Order #{self.order.id}'

    def __repr__(self):
        return f'<OrderItem id={self.id}, product="{self.product.name}", quantity={self.quantity}, cost={self.get_cost()}>'

    def get_cost(self):
        """Calculate the cost of this order item."""
        return self.price * self.quantity