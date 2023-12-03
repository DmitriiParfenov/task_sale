from django.contrib import admin

from sales.models import Sale


# Register your models here.
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'unit', 'supplier', 'created', 'sale_user', 'debt')
    list_display_links = ('id',)
    search_fields = ('title', 'created', 'contact__city')
    list_filter = ('title', 'created', 'contact__city')
    actions = ['admin_action']

    @admin.action(description='Погашение задолженностей')
    def admin_action(self, request, queryset):
        queryset.update(debt=0.00)
