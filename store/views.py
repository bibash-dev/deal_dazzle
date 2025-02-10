from django.shortcuts import render, get_object_or_404

from cart.forms import CartAddProductForm
from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).select_related('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'product/product_list.html',
                  {'category': category, 'categories': categories, 'products': products})


def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'product/product_detail.html', {'product': product, 'cart_product_form': cart_product_form})
