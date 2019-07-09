from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from store.forms import OrderForm
from store.models import Entry, Order, Product


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
            return redirect('profile:profile')
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

