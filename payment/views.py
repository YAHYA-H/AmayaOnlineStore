import braintree
from orders.models import Order
from django.shortcuts import render, redirect, get_object_or_404


def payment_process(request):
    order_id = request.session.get(
        'order_id')  # get the current order from session key
    order = get_object_or_404(Order, id=order_id)  # retrieve the Order object
    if request.method == 'POST':
        # retrieve the nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = braintree.Transaction.sale({
            'amount':
            '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce':
            nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:cancelled')
    else:
        # generate token
        client_token = braintree.ClientToken.generate()
        return render(request, 'payment/process.html', {
            'order': order,
            'client_token': client_token
        })


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_cancelled(request):
    return render(request, 'payment/cancelled.html')