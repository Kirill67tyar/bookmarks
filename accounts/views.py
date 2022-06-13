from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    login, logout,
    authenticate,
    get_user_model,
)

from accounts.forms import LoginForm

from images.utils import get_object_or_null

User = get_user_model()


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd.get('username')
            password = cd.get('password')

            user = authenticate(
                request,
                username=username,
                password=password
            )
            login(request, user)
            return redirect('accounts:dashboard')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('accounts:login')


@login_required
def dashboard_view(request):
    ctx = {
        'action': 'dashboard',
    }
    return render(
        request=request,
        template_name='accounts/dashboard.html',
        context=ctx
    )

class MyPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('accounts:password_change_done')
