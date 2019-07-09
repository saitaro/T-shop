from django.shortcuts import render, redirect
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
    return redirect('store:cart')


# @force_http
@login_required
def cart(request):
    cart = request.session.get('cart', {})
    entries = [Entry(product=Product.objects.get(pk=pk),
                     quantity=cart[pk]) for pk in cart]
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order(customer=request.user)
            order.address = form.cleaned_data['address']
            order.save()
            for entry in entries:
                entry.order = order
            Entry.objects.bulk_create(entries)
            messages.add_message(request, 777, f'Thanks for shopping! Your order was created with ID: {order.pk}.')
            request.session['cart'] = {}
            return redirect('store:profile')
    else:
        data = {'name': request.user.name,
                'phone': request.user.phone}
        form = OrderForm(initial=data)

    total_price = sum(entry.price for entry in entries)
    context = {
        'entries': entries,
        'total_price': total_price,
        'form': form,
        'cart': sum(request.session.get('cart', {}).values()),
    }
    return render(request, 'cart.html', context)


# @force_https
@login_required
def profile(request):
    context = {
        'orders': Order.objects.filter(customer=request.user),
        'cart': sum(request.session.get('cart', {}).values()),
    }
    return render(request, 'profile.html', context)
