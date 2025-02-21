import itertools
import redis
from django.conf import settings
from .models import Product

# establish a connection with redis
try:
    redis_connection = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
    )
except redis.ConnectionError as e:
    raise Exception("Redis connection failed") from e


class ProductRecommender:
    def get_product_key(self, product_id):
        return f"product:{product_id}:purchased with"

    def products_bought_together(self, products):
        product_ids = [product.id for product in products]
        unique_product_ids = set(product_ids)

        for product_id, with_id in itertools.combinations(unique_product_ids, 2):
            redis_connection.zincrby(self.get_product_key(product_id), 1, with_id)
            redis_connection.zincrby(self.get_product_key(with_id), 1, product_id)

    def fetch_recommended_products(self, products, max_results=6):
        product_ids = [product.id for product in products]
        if len(products) == 1:
            # single product
            recommendations = redis_connection.zrange(self.get_product_key(product_ids[0]), 0, -1, desc=True)[
                              :max_results]
        else:
            flat_ids = ''.join([str(id) for id in product_ids])
            temp_key = f"tmp_{flat_ids}"
            # multiple products, combine score of all products
            # store the resulting sorted set in a temporary key
            keys = [self.get_product_key(id) for id in product_ids]
            redis_connection.zunionstore(temp_key, keys)
            # remove ids for the products the recommendation is for
            redis_connection.zrem(temp_key, *product_ids)
            # get the product ids by their score, descendant sort
            recommendations = redis_connection.zrange(temp_key, 0, -1, desc=True)[:max_results]
            # remove the temporary key
            redis_connection.delete(temp_key)
        recommended_products_ids = [int(id) for id in recommendations]
        # get suggested products and sort by order of appearance
        recommended_products = list(Product.objects.filter(id__in=recommended_products_ids))
        recommended_products.sort(key=lambda product: recommended_products_ids.index(product.id))
        return recommended_products
