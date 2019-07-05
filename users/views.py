from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, ModelForm, PasswordInput, TextInput
from django.shortcuts import redirect, render


class CreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = 'email', 'name'


def register(request):
    if request.method == "POST":
        form = CreationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            messages.success(request, f'Your account created, {name}! Now you can log in.')
            form.save()
            return redirect('main:cian_render')
    else:
        form = CreationForm()
    
    return render(request, 'users/register.html', {'form': form})

def profile(request):
    user = request.user
    return render(request, 'users/profile.html',
                  {'favs': user.favorites.all()})

@login_required(login_url='login')
def add_favorite(request, pk):
    user = request.user
    fav = user.favorites.filter(pk=pk)
    if fav:
        user.favorites.remove(pk)
    else: 
        user.favorites.add(pk)
    # print(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))