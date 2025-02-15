from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # URL pattern for viewing the cart details
    path('', views.cart_detail, name='cart_detail'),

    # URL pattern for adding a product to the cart
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),

    # URL pattern for removing a product from the cart
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]
