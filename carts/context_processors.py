from .models import CartItem, Carts
from .views import _cart_id

def counter(request):

    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Carts.objects.filter(cart_id = _cart_id(request))
            cart_items = CartItem.objects.all().filter(cart = cart[:1])

            cart_count = 0

            for cart_item in cart_items:
                cart_count += cart_item.quantity

        except Carts.DoesnNotExist:
            cart_count = 0

    return dict(cart_count=cart_count)
    