from django.contrib import admin
from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.


class OrderItemInline(admin.TabularInline):
    # an inline allows us to include a model on the same edit page its related model
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name', 'email', 'address', 'postal_code',
        'city', 'paid', 'created', 'updated'
    ]
    last_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]