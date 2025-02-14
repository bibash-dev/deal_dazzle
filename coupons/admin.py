from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'valid_from', 'valid_to', 'discount', 'active')
    list_filter = ('active', 'valid_from', 'valid_to')
    search_fields = ('code',)
    list_editable = ('active',)
    date_hierarchy = 'valid_from'

    fieldsets = (
        (None, {
            'fields': ('code', 'discount', 'active')
        }),
        ('Validity Period', {
            'fields': ('valid_from', 'valid_to'),
            'description': 'Define the time period during which the coupon is valid.',
        }),
    )
