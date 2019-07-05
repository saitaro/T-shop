from collections import defaultdict, Counter

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, reverse
from django.template import Context

# from .forms import ProductForm
from .models import Product


def catalog(request):
    context = {
        'products': Product.objects.all(),
    }
    return render(request, 'catalog.html', context)


def cart(request):
    cart = request.session.get('cart', {})
    # total_price = Product.objects.filter(id__in=cart.keys())
    # quantities = cart.values()

    context = {
        'cart': cart,
        # 'cart': cart_contents,
        # 'quantities': quantities,
    }
    return render(request, 'cart.html', context)


def add_to_cart(request, name):
    cart = request.session.get('cart', {})
    if cart.get(name):
        cart[name] += 1
    else:
        cart[name] = 1

    request.session['cart'] = cart
    request.session.modified = True
    print(cart)
    return redirect('store:catalog')
