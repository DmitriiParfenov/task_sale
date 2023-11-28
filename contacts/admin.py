from django.contrib import admin

# Register your models here.
from contacts.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'country', 'city', 'street', 'number')
    list_display_links = ('id',)
    search_fields = ('country', 'city')
    list_filter = ('country', 'city')
