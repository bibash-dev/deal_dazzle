from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Product


def product_list(request, category_slug=None):
    """
    Display a list of available products, optionally filtered by category.
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).select_related('category')

    # Filter products by category if a category slug is provided
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'product/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })


def product_detail(request, category_slug, slug):
    """
    Display the details of a specific product, including a form to add it to the cart.
    """
    product = get_object_or_404(
        Product,
        category__slug=category_slug,
        slug=slug,
        available=True
    )
    cart_product_form = CartAddProductForm()

    return render(request, 'product/product_detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
    })