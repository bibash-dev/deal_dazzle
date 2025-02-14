import weasyprint
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created


def order_create(request):
    """
    View to handle orders creation.
    """
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    if cart.coupon:
                        order.coupon = cart.coupon
                        order.discount = cart.coupon.discount
                    order.save()
                    # Create orders items from the cart
                    for item in cart:
                        OrderItem.objects.create(
                            order=order,
                            product=item['product'],
                            price=item['price'],
                            quantity=item['quantity'],
                        )
                    cart.clear()
                    # Launch the asynchronous task to send an orders confirmation email
                    order_created.delay(order.id)
                    # Store the orders ID in the session for payment processing
                    request.session['order_id'] = order.id

                    return redirect("payment:process")

            except Exception as e:
                print(f"Exception occurred: {str(e)}")
                messages.error(request, "An error occurred while processing your orders. Please try again.")
                return redirect("cart:cart_detail")

    else:
        # If it's a GET request, initialize an empty form
        form = OrderCreateForm()

    # Render the orders creation page
    return render(
        request,
        'order_create.html',
        {'cart': cart, 'form': form},
    )


@staff_member_required
def admin_order_detail(request, order_id):
    """
    View to display the details of a specific orders in the admin interface.
    Only accessible by staff members.
    """
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
        'order_items': order.items.all(),  # Include related orders items
    }
    return render(request, 'admin/orders/order/detail.html', context)


@staff_member_required
def admin_order_pdf(request, order_id):
    """
    Generates a PDF for a specific order.
    """
    order = get_object_or_404(Order, id=order_id)

    # Render the HTML template with the order context
    html = render_to_string('admin/orders/order/pdf.html', {'order': order})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'

    # Generate the PDF
    try:
        weasyprint.HTML(string=html).write_pdf(response)
    except Exception as e:
        return HttpResponse(f"Failed to generate PDF: {str(e)}", status=500)

    return response
