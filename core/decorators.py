from django.http import HttpResponseBadRequest

def http_methods_only(methods=['POST', 'GET']):
    def wrap(f):
        def _wrap(request, *args, **kwargs):
            if not request.method in methods:
                return HttpResponseBadRequest()
            return f(request, *args, **kwargs)
        return _wrap
    return wrap

def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax:
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    return wrap

