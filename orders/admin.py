import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from django.contrib import admin
from .models import Order, OrderItem
from django.urls import reverse
from django.utils.safestring import mark_safe


class OrderItemInline(admin.TabularInline):
    # an inline allows us to include a model on the same edit page its related model
    model = OrderItem
    raw_id_fields = ['product']


# generic admin action that can be added to any ModelAdmin class.
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(
        content_type='text/csv'
    )  # tell browser that that the resp has to be treated as a CSV file
    response['Content-Disposition'] = 'attachment;'\
        'filename={}.csv'.format(opts.verbose_name
        ) # Indicate that the HTTP response contains an attached file
    writer = csv.writer(
        response)  # create a csv obj that will write on the resp obj
    fields = [
        field for field in opts.get_fields(
        )  # get the fields dynamically with `get_fields` of the model `-meta` options
        if not field.many_to_many and not field.one_to_many
    ]
    # write a first row with  header info -->(write header row including the fields names)
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:  #<- iterate over queryset  and write a row for each obj return by queryset
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime(
                    '%d./%m/%Y'
                )  # take care of formatting by datetime obj b/c the ouput value for csv has to be a str
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'  # customize the display name for the action in the template


def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(
        reverse('orders:admin_order_detail', args=[obj.id])))


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name', 'email', 'address', 'postal_code',
        'city', 'paid', 'created', 'updated', order_detail
    ]
    last_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]  # Exporting orders to CSV files
