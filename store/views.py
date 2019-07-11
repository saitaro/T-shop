from django.shortcuts import render, redirect

from .forms import CategoryForm
from .models import Product, Category
from .decorators import force_http, force_https


# @force_http
def catalog(request):
    if request.GET:
        form = CategoryForm(request.GET)
        form.is_valid()
        choices = form.cleaned_data['categories']
        request.session['categories'] = choices
        products = Product.objects.filter(category__id__in=choices)
    else:
        if request.session.get('add') and request.session.get('categories'):
            choices = request.session['categories']
            form = CategoryForm({'categories': choices})
            products = Product.objects.filter(category__id__in=choices)
        else:
            if request.session.get('categories'):
                request.session['categories'].clear()
            form = CategoryForm()
            products = Product.objects.all()
        request.session['add'] = False

    context = {
        'products': products,
        'form': form,
        'cart': sum(request.session.get('cart', {}).values()),
    }
    return render(request, 'catalog.html', context)


# @force_http
def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    cart[pk] = cart.get(pk, 0) + 1
    request.session['cart'] = cart
    request.session['add'] = True
    return redirect('store:catalog')

    