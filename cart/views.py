from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib import messages
from store.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import ApplyCouponForm
from store.product_recommender import ProductRecommender



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
        quantity = cleaned_data["quantity"]
        override = cleaned_data["override"]

        # Add or update the product in the cart
        cart.add(
            product=product,
            quantity=quantity,
            override=override,
        )

    # Redirect to the cart detail page
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
                "override": True
            }
        )

    shipping_cost = cart.get_shipping_cost()
    apply_coupon_form = ApplyCouponForm()

    recommender = ProductRecommender()
    cart_products = [item['product'] for item in cart] if cart else []
    recommended_products = recommender.fetch_recommended_products(cart_products, 4) if cart_products else []

    return render(request, "cart_detail.html",
                  {"cart": cart, "apply_coupon_form": apply_coupon_form, "recommended_products": recommended_products, "shipping_cost": shipping_cost})
