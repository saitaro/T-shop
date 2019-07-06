from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import OrderForm, CategoryForm
from .models import Product, Entry, Order, Category


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
    }
    return render(request, 'catalog.html', context)


def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    if cart.get(pk):
        cart[pk] += 1
    else:
        cart[pk] = 1

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('store:catalog')


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
            messages.success(request, f'Thanks for shopping! Order #{order.pk} has been created.')
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
    }
    return render(request, 'cart.html', context)


@login_required
def profile(request):
    context = {
        'orders': Order.objects.filter(customer=request.user),
    }
    return render(request, 'profile.html', context)
