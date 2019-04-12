from decimal import Decimal
from django.conf import settings
from store.models import Product


class Cart(object):
    def __init__(self, request):
        """initialize the cart"""
        self.session = request.session  # store the current session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart to the session
            cart = self.session.get[settings.CART_SESSION_ID] = {}
        self.cart = cart
