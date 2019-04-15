# context processor- to include the current cart in the
# request context(i.e available globally to all templates )
from .cart import Cart


def cart(request):
    return {'cart': Cart(request)}
