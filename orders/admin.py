import csv
from datetime import datetime
from django.http import HttpResponse
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Order, OrderItem


def export_to_csv(modeladmin, request, queryset):
    """
    Exports the selected queryset to a CSV file.
    """
    model = modeladmin.model
    opts = model._meta
    filename = f"{opts.verbose_name}.csv"
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={filename}'

    # Define fields to export, excluding relational fields
    fields = [
        field for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]

    # Create CSV writer
    writer = csv.writer(response)

    # Write header row
    headers = [field.verbose_name for field in fields]
    writer.writerow(headers)

    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            # Format datetime fields
            if isinstance(value, datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(str(value))
        writer.writerow(data_row)

    return response


export_to_csv.short_description = 'Export to CSV'


def order_payment(obj):
    """
    Returns a link to the Stripe payment dashboard for the given object.
    If the object does not have a Stripe ID, returns an empty string.
    """
    if not obj.stripe_id:
        return ''

    url = obj.get_stripe_url()
    return format_html(
        '<a href="{}" target="_blank" rel="noopener noreferrer">{}</a>',
        url, obj.stripe_id
    )


order_payment.short_description = 'Stripe Payment'


def order_detail(obj):
    """
    Returns a link to the admin detail page for the given order object.
    """
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return format_html('<a href="{}">View</a>', url)


order_detail.short_description = 'View Details'


def order_pdf(obj):
    """
    Generates a link to the PDF invoice for the given order object.
    """
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return format_html('<a href="{}" target="_blank">PDF</a>', url)


order_pdf.short_description = 'Invoice'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0  # Prevents extra blank forms from being displayed


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'address',
        'postal_code',
        'city',
        'paid',
        order_payment,
        'created_at',
        'updated_at',
        order_detail,
        order_pdf,
    ]
    list_filter = ['paid', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
    list_select_related = True
    search_fields = ['first_name', 'last_name', 'email']
    date_hierarchy = 'created_at'
