from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Coupon Code")
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Discount Percentage",
        help_text="Discount percentage value (0 to 100)"
    )
    active = models.BooleanField(default=True, verbose_name="Is Active")

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"
        ordering = ["-valid_from"]

    def __str__(self):
        return self.code

    def clean(self):
        if self.valid_from and self.valid_to and self.valid_from >= self.valid_to:
            raise ValidationError({"valid_to": "Valid To must be after Valid From."})

    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to
