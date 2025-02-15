from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Product
from .product_recommender import ProductRecommender

RECOMMENDED_PRODUCTS_LIMIT = 4


def product_list(request, category_slug=None):
    """Display a list of products, optionally filtered by category."""
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).select_related('category')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'product/product_list.html', context)


def product_detail(request, id, slug):
    """Display details of a specific product and recommendations."""
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    recommender = ProductRecommender()
    recommended_products = recommender.fetch_recommended_products([product], RECOMMENDED_PRODUCTS_LIMIT)

    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'recommended_products': recommended_products,
    }
    return render(request, 'product/product_detail.html', context)
