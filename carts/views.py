from math import prod
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from store.models import Product, Variation
from .models import Carts, CartItem

def cart(request, total = 0 , quantity = 0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        cart = Carts.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (18*total)/100
        grand_total = total + tax
        
    except Carts.DoesNotExist:
        pass
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'store/cart.html', context)


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):

    # color = request.GET['color'];
    # size = request.GET['size'];

    # return HttpResponse(color + '  ' + size)

    product = Product.objects.get(id=product_id)
    product_variation = []

    if request.method == 'POST':
        
        for item in request.POST:
            key = item
            value = request.POST.get(key)

            try:
                variation = Variation.objects.get(product = product, variation_category__iexact=key, vartiation_value__iexact=value)

                product_variation.append(variation)
            except:
                pass

    
    try:
        cart = Carts.objects.get(cart_id = _cart_id(request))
    except Carts.DoesNotExist:
        cart = Carts.objects.create(
            cart_id = _cart_id(request)
        )
    
    cart.save()

    is_cart_item_exists = CartItem.objects.filter(product=product, cart = cart).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product,cart=cart)

        ex_variation_list = []
        ide = []

        for item in cart_item:
            existing_variations = item.variations.all()
            ex_variation_list.append(list(existing_variations))
            ide.append(item.id)


        if product_variation in ex_variation_list:

            index = ex_variation_list.index(product_variation)
            item_id = ide[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.save()

        else:
            item = CartItem.objects.create(product=product, quantity = 1, cart = cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
                # for item in product_variation:
                #     cart_item.variations.add(item)
            # cart_item.quantity += 1
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            for item in product_variation:
                cart_item.variations.add(item)
        cart_item.save()
    
    return redirect('cart')


def remove_cart(request, product_id):

    cart = Carts.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

def remove_cart_item(request, product_id):

    cart = Carts.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(
        product = product, cart = cart
    )

    cart_item.delete()

    return redirect('cart')