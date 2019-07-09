from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import OrderForm, CategoryForm
from .models import Product, Entry, Order, Category
from .decorators import force_http, force_https


# @force_http
def catalog(request):
    if request.GET:
        categories = CategoryForm(request.GET)
        choices = dict(categories.data)['categories']
        products = Product.objects.filter(category__id__in=choices)
    else:
        categories = CategoryForm()
        products = Product.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'cart': sum(request.session.get('cart', {}).values()),
    }
    return render(request, 'catalog.html', context)


# @force_http
def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    cart[pk] = cart.get(pk, 0) + 1
    request.session['cart'] = cart
    return redirect('store:catalog')


def remove_from_cart(request, pk):
    cart = request.session['cart']
    del cart[pk]
    request.session.modified = True
    return redirect('cart:cart')
