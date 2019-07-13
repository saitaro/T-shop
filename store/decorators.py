from django.http import HttpResponseRedirect


def force_http(view):
    def wrapper(request, *args, **kwargs):
        if request and request.is_secure():
            # if request.META.get('HTTP_X_FORWARDED_PROTO'):
            #     request.META['HTTP_X_FORWARDED_PROTO'] = 'http'
            url = request.build_absolute_uri()
            url = url.replace('https', 'http')
            # return HttpResponseRedirect(url)
        return view(request, *args, **kwargs)
    return wrapper

