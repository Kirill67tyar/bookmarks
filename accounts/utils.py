from functools import wraps

from django.shortcuts import redirect


def anonymous_requeired(func):
    @wraps(func)
    def dec(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return redirect('accounts:dashboard')

    return dec
