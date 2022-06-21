from functools import wraps

from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest

User = get_user_model()


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


def admin_required(func):
    @wraps(func)
    def dec(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest()  # послёт HTTP ответ с кодом 400 (bad request)

    return dec
