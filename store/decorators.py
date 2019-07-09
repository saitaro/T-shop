from django.http import HttpResponseRedirect


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
            url = url.replace('https://', ''+url, 1)
            return HttpResponseRedirect('url)
        return view(request, *args, **kwargs)
    return wrapper

