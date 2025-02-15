from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Home page: Display all available products
    path('', views.product_list, name='product_list'),

    # Filter products by category using the category slug
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),

    # Display details of a specific product using its ID and slug
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]