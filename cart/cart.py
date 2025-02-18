from django.conf import settings
from decimal import Decimal
from store.models import Product
from coupons.models import Coupon


class Cart:
    def __init__(self, request):
        """
        Initialize the cart using the session from the request.
        If no cart exists in the session, create an empty one.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # Store current applied coupon
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, override=False):
        """
        Add a product to the cart or update its quantity.
        If override_quantity is True, set the quantity directly.
        Otherwise, increment the existing quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
                "name": product.name,
            }

        if override:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        self.save()

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """
        Remove the entire cart from the session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def save(self):
        """
        Mark the session as modified to ensure it gets saved.
        """
        self.session.modified = True

    def __iter__(self):
        """
        Iterate over the items in the cart and fetch the corresponding products
        from the database. Calculate the total price for each item.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        # Add product objects and calculate total prices
        for product in products:
            cart_item = cart[str(product.id)]
            cart_item["product"] = product
            cart_item["price"] = Decimal(cart_item["price"])
            cart_item["total_price"] = cart_item["price"] * cart_item["quantity"]
            yield cart_item

    def __len__(self):
        """
        Return the total number of items in the cart.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_weight(self):
        """Calculate the total weight of all items in the cart."""
        total_weight = Decimal('0')
        for item in self.cart.values():
            product = item['product']
            quantity = item['quantity']
            total_weight += product.weight * quantity
        return total_weight

    def get_shipping_cost(self):
        """Calculate the shipping cost based on the total weight."""
        total_weight = self.get_total_weight()
        # Shipping cost logic here: $5 for the first 500g, $1 for each additional 100g
        if total_weight <= 500:
            return Decimal('5.00')
        else:
            additional_weight = total_weight - 500
            additional_cost = (additional_weight // 100) * Decimal('1.00')
            return Decimal('5.00') + additional_cost

    def get_total_price(self):
        """
        Calculate and return the total price of all items in the cart.
        """
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (
                    self.coupon.discount / Decimal(100)
            ) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()

    def get_total_price_after_discount_and_shipping_cost(self):
        return self.get_total_price_after_discount() + self.get_shipping_cost()
