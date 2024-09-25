from django.shortcuts import render, redirect
from store.models import Product
from .models import Cart, CartItem
from django.db.models import Q
# Create your views here.


def create_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def cart(request):
    cart_items = None
    tax = 0
    total = 0
    grand_total = 0
    session_id = create_session(request)
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            total += item.product.price * item.quantity
    else:
        cartid = Cart.objects.get(cart_id=session_id)
        cart_id = Cart.objects.filter(cart_id=session_id).exists()
    
        if cart_id:
            cart_items = CartItem.objects.filter(cart=cartid)
            for item in cart_items:
                total += item.product.price * item.quantity
                
    tax = (total * 2) / 100
    grand_total = total + tax
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'tax' : tax, 'total' : total, 'grand_total' : grand_total})


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    session_id = create_session(request)
    
    if request.user.is_authenticated:
         cart_item = CartItem.objects.filter(product=product, user=request.user).exists()
         if cart_item:
            item = CartItem.objects.get(product=product)
            item.quantity += 1
            item.save()
         else:
            cartid = Cart.objects.get(cart_id=session_id)
            item = CartItem.objects.create(
                cart = cartid,
                product = product,
                quantity = 1,
                user = request.user
            )
            item.save()
    else:
        cart_id = Cart.objects.filter(cart_id = session_id).exists()
        if cart_id:
            cartid = Cart.objects.get(cart_id=session_id)
            cart_item = CartItem.objects.filter(product=product, cart=cartid).exists()
            if cart_item:
                item = CartItem.objects.get(product=product)
                item.quantity += 1
                item.save()
            else:
                cartid = Cart.objects.get(cart_id=session_id)
                print('assdf ', cartid, session_id)
                item = CartItem.objects.create(
                    cart = cartid,
                    product = product,
                    quantity = 1
                )
                item.save()
        else:
            cart = Cart.objects.create(
                cart_id = session_id 
            )
            cart.save()

    return redirect('cart')


def remove_cart_item(request, product_id):
    print(product_id)
    product = Product.objects.get(id=product_id)
    session_id = request.session.session_key
    cartid = Cart.objects.get(cart_id=session_id)
    cart_item = CartItem.objects.get(cart=cartid, product=product)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    session_id = request.session.session_key
    cartid = Cart.objects.get(cart_id=session_id)
    cart_item = CartItem.objects.get(cart=cartid, product=product)
    
    cart_item.delete()
    return redirect('cart')


