from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib import messages
from store.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import ApplyCouponForm


@require_POST
def cart_add(request, product_id):
    """
    Add a product to the cart or update its quantity.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        cart.add(
            product=product,
            quantity=cleaned_data["quantity"],
            override_quantity=cleaned_data["override"],
        )
        messages.success(request, f"{product.name} has been added to your cart.")
    else:
        messages.error(request, "Invalid form submission. Please try again.")

    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    """
    Remove a product from the cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f"{product.name} has been removed from your cart.")
    return redirect("cart:cart_detail")


def cart_detail(request):
    """
    Display the contents of the cart.
    """
    cart = Cart(request)

    # Add update forms to each cart item
    for item in cart:
        item["update_quantity_form"] = CartAddProductForm(
            initial={
                "quantity": item["quantity"],
                "override": True,
            }
        )
    apply_coupon_form = ApplyCouponForm()

    return render(request, "cart_detail.html", {"cart": cart, "apply_coupon_form": apply_coupon_form})
