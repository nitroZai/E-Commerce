from django.shortcuts import render, get_object_or_404
from carts.models import CartItem, Carts
from store.models import Product
from carts.views import _cart_id

def home(request):

    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products
    }

    return render(request, 'home.html', context)

def cart_count(request):
    
    product = Product.objects.get(product = product)
    cart = Carts.objects.get(cart_id = _cart_id(request))

    cart_items = CartItem.objects.filter(product=product, cart = cart)
    total_count = 0
    for cart_item in cart_items:
        total_count += cart_item.quantity

    context = {
        'count': total_count
    }

    return render(request, 'includes/navbar.html', context)