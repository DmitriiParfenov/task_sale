from django.contrib import admin

from products.models import Product


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'model', 'release')
    list_display_links = ('id',)
    search_fields = ('title', 'release')
    list_filter = ('title', 'release')
