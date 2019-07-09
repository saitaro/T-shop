from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


def force_https(view):
    def wrapper(request, *args, **kwargs):
        if request and not request.is_secure():
            url = request.build_absolute_uri(request.get_full_path())
            if url.startswith('http://'):
                url = url.replace('http://', 'https://', 1)
            else:
                url = 'https://' + url
            return HttpResponseRedirect(url)
        return view(request, *args, **kwargs)
    return wrapper


def force_http(view):
    def wrapper(request, *args, **kwargs):
        if request and request.is_secure():
            url = request.get_full_path()
            print('OLD:', url)
            url = url.replace('https://', '123///'+url, 1)
            print('NEW', url)
            # return HttpResponseRedirect(url)
            return HttpResponseRedirect('yandex.ru')
        # return view(request, *args, **kwargs)
        return HttpResponseRedirect('google.com')
    return wrapper

