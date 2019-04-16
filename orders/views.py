from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse


@staff_member_required  # (checks both `is_active` and `is_staff` fields are `True`)
def admin_order_detail(request, order_id):
    # for custom admin view
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


def order_create(request):
    cart = Cart(request)  # obtain the current cart from the session
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                #clear the cart
                cart.clear()
                # launch async task
                order_created.delay(order.id)
                # set the order in session
                request.session['order_id'] = order.id
                # redirect for payment
                return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
        return render(request, 'orders/order/create.html', {
            'form': form,
            'cart': cart
        })
