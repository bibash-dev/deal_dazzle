from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available','weight', 'created_at', 'updated_at']
    list_filter = ['category', 'available', 'created_at', 'updated_at']
    list_editable = ['price', 'available', 'weight']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'slug']
    date_hierarchy = 'created_at'
