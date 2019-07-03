from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from .forms import ImageForm
from .models import Image


def index(request):
    context = {
        'images': Image.objects.all(),
    }
    return render(request, 'index.html', context)


def index_list(request):
    context = {
        'images': Image.objects.all(),
    }
    return render(request, 'index_list.html', context)


def upload(request):
    form = ImageForm()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            user = user if not user.is_anonymous else None
            form.save(user)
            return redirect('index')

    context = {
        'form': form,
    }
    if form.errors:
        context['file_error'] = form.errors['file'].as_text().strip('* ')

    return render(request, 'upload.html', context)
