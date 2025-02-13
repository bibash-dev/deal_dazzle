from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created


def order_create(request):
    """
    View to handle order creation.
    """
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save()
                    # Create order items from the cart
                    for item in cart:
                        OrderItem.objects.create(
                            order=order,
                            product=item['product'],
                            price=item['price'],
                            quantity=item['quantity'],
                        )
                    cart.clear()
                    # Launch the asynchronous task to send an order confirmation email
                    order_created.delay(order.id)
                    # Store the order ID in the session for payment processing
                    request.session['order_id'] = order.id

                    return redirect("payment:process")

            except Exception as e:
                messages.error(request, "An error occurred while processing your order. Please try again.")
                return redirect("cart:cart_detail")

    else:
        # If it's a GET request, initialize an empty form
        form = OrderCreateForm()

    # Render the order creation page
    return render(
        request,
        'order_create.html',
        {'cart': cart, 'form': form},
    )
