import re

import requests
from django import forms
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from .models import Image


class ImageForm(forms.Form):
    name = forms.CharField(max_length=128, required=False)
    description = forms.CharField(max_length=128, required=False)
    url = forms.URLField(required=False, label='URL')
    file = forms.ImageField(required=False)

    def clean_file(self):
        file = self.cleaned_data.get('file')
        url = self.data.get('url')

        if file and url:
            raise forms.ValidationError('Cannot use both File and URL fields.')
        elif not (file or url):
            raise forms.ValidationError('Please use either File or URL field.')
        elif url and requests.get(url).status_code != 200:
            raise forms.ValidationError('Image unavailable.')
        elif url:
            filename = url.split('/')[-1]
            pattern = re.compile(r'.+\.(jpeg|jpg|png|gif|tiff|tif)', re.IGNORECASE)
            if not pattern.search(filename):
                raise forms.ValidationError('Image type must be JPEG, TIFF, PNG or GIF.')
        else:
            return file or url

    def save(self, user=None):
        data = dict(self.data, **self.cleaned_data)
        name = data.get('name')
        description = data.get('description')
        url = data.get('url')

        if url:
            request = requests.get(url)
            temp = NamedTemporaryFile()
            filename = url.split('/')[-1]
            pattern = re.compile(r'.+\.(jpeg|jpg|bmp|png|gif)', re.IGNORECASE)
            filename = pattern.search(filename)[0]

            for block in request.iter_content(1024 * 4):
                if not block:
                    break
                temp.write(block)

            file = File(temp, name=filename)

        else:
            file = data.get('file')

        Image.objects.create(
            name=name,
            description=description,
            uploader=user,
            file=file,
        )
