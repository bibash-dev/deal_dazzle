import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from orders.models import Order
from .tasks import payment_completed
from store.models import Product
from store.product_recommender import ProductRecommender


@require_POST
@csrf_exempt
def stripe_webhook(request):
    """
    Handle Stripe webhook events, particularly for completed payments.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            return handle_successful_payment(session)

    return HttpResponse(status=200)


def handle_successful_payment(session):
    """
    Handle a successful payment event from Stripe.

    Args:
        session: The Stripe checkout session object.
    """
    try:
        order = Order.objects.get(id=session.client_reference_id)
    except Order.DoesNotExist:
        return HttpResponse(status=404)

    # Mark the order as paid and store the Stripe payment ID
    order.paid = True
    order.stripe_id = session.payment_intent
    order.save()

    # Update product recommendations
    product_ids = order.items.values_list('product_id', flat=True)
    products = Product.objects.filter(id__in=product_ids)
    recommender = ProductRecommender()
    recommender.products_bought_together(products)

    # Launch asynchronous task to handle post-payment actions
    payment_completed.delay(order.id)

    return HttpResponse(status=200)
