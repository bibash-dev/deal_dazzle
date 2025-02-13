import stripe
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    """
    View to handle the payment process using Stripe Checkout.
    """
    order_id = request.session.get('order_id')
    if not order_id:
        messages.error(request, "No order found. Please place an order first.")
        return redirect('orders:order_create')

    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        try:
            success_url = request.build_absolute_uri(reverse('payment:completed'))
            cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

            # Prepare line items for the Stripe session
            line_items = []
            for item in order.items.all():
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.product.name,
                        },
                        'unit_amount': int(item.price * Decimal('100')),
                    },
                    'quantity': item.quantity,
                })

            session_data = {
                'mode': 'payment',
                'client_reference_id': order.id,
                'success_url': success_url,
                'cancel_url': cancel_url,
                'line_items': line_items,
            }

            session = stripe.checkout.Session.create(**session_data)
            return redirect(session.url, code=303)

        except stripe.error.StripeError as e:
            messages.error(request, f"An error occurred while processing your payment: {e.user_message}")
            return redirect('orders:order_detail', order_id=order.id)

        except Exception as e:
            messages.error(request, "An unexpected error occurred. Please try again.")
            return redirect('orders:order_detail', order_id=order.id)

    else:
        return render(request, 'payment/process.html', locals())


def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
