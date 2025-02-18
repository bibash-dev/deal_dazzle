from django.shortcuts import render, get_object_or_404
from django.db.models import Min, Max
from cart.forms import CartAddProductForm
from .models import Category, Product
from .product_recommender import ProductRecommender

# Number of recommended products
RECOMMENDED_PRODUCTS_LIMIT = 4

# Sorting options
SORT_BY_NEWEST = "newest"
SORT_BY_PRICE_LOW = "price-low"
SORT_BY_PRICE_HIGH = "price-high"

SORT_OPTIONS = {
    SORT_BY_NEWEST: "-created_at",
    SORT_BY_PRICE_LOW: "price",
    SORT_BY_PRICE_HIGH: "-price",
}


def filter_products(products, min_price=None, max_price=None):
    if min_price is not None:
        products = products.filter(price__gte=min_price)
    if max_price is not None:
        products = products.filter(price__lte=max_price)
    return products


def sort_products(products, sort_by=None):
    if sort_by in SORT_OPTIONS:
        return products.order_by(SORT_OPTIONS[sort_by])
    return products


def get_price_range(products):
    return products.aggregate(min_price=Min('price'), max_price=Max('price'))


def parse_price(price):
    if price is not None:
        try:
            return float(price)
        except (ValueError, TypeError):
            return None
    return None


def product_list(request, category_slug=None):
    """Display a list of products, optionally filtered by category."""
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).select_related('category')

    # Filter by category if provided
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Parse and validate price range inputs
    min_price = parse_price(request.GET.get('min_price'))
    max_price = parse_price(request.GET.get('max_price'))

    # Apply price range filter
    products = filter_products(products, min_price, max_price)

    # Apply sorting
    sort_by = request.GET.get('sort_by')
    products = sort_products(products, sort_by)

    # Get price range for the filtered products
    price_range = get_price_range(products)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'price_range': price_range,
        'sort_by': sort_by,
        'min_price': min_price,
        'max_price': max_price,
    }
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'product/partials/product_list.html', context)
    else:
        return render(request, 'product/product_list.html', context)


def product_detail(request, id, slug):
    """Display details of a specific product and recommendations."""
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    # Fetch recommended products
    recommender = ProductRecommender()
    recommended_products = recommender.fetch_recommended_products(
        [product], RECOMMENDED_PRODUCTS_LIMIT
    )

    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'recommended_products': recommended_products,
    }
    return render(request, 'product/product_detail.html', context)
