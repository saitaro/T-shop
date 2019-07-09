from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from store.models import Order


@login_required
def profile(request):
    context = {
        'orders': Order.objects.filter(customer=request.user),
        'cart': sum(request.session.get('cart', {}).values()),
    }
    return render(request, 'profile.html', context)
