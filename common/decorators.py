from functools import wraps

from django.shortcuts import redirect
from django.http import HttpResponseBadRequest


def anonymous_required(func):
    @wraps(func)
    def dec(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest()  # послёт HTTP ответ с кодом 400 (bad request)

    return dec


def ajax_required(func):
    @wraps(func)
    def dec(request, *args, **kwargs):
        # if request.is_ajax(): # is_ajax() больше нету
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return func(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest()  # послёт HTTP ответ с кодом 400 (bad request)

    return dec
