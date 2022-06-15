from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    login, logout,
    authenticate,
    get_user_model,
)
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from accounts.models import Profile
from accounts.utils import anonymous_requeired
from accounts.forms import (
    LoginForm,
    UserModelForm,
    ProfileModelForm,
    UserRegistraionModelForm,
)
from images.utils import (
    p_dir, p_mro, p_glob, p_loc, p_type,
    delimiter, p_content, show_builtins, show_doc, console_compose,
)

# p_dir, p_mro, p_glob, p_loc, p_content, show_builtins, show_doc, delimiter

User = get_user_model()


@anonymous_requeired
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


@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def dashboard_view(request):
    ctx = {
        'action': 'dashboard',
    }

    # --- for console ---
    # console_compose(request)
    # --- for console ---

    return render(
        request=request,
        template_name='accounts/dashboard.html',
        context=ctx
    )


@anonymous_requeired
def register_view(request):
    if request.method == 'POST':
        form = UserRegistraionModelForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            new_user = form.save(commit=False)
            new_user.set_password(password)
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'accounts/register_done.html', {'new_user': new_user, })
    else:
        form = UserRegistraionModelForm()
    return render(request, 'accounts/register.html', {'form': form, })


@login_required
def edit_view(request):
    user = request.user
    if request.method == 'POST':
        user_form = UserModelForm(
            instance=user,
            data=request.POST
        )
        profile_form = ProfileModelForm(
            instance=user.profile,
            data=request.POST,
            files=request.FILES,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request=request, message='Profile updated successfully')
        else:
            messages.error(request=request, message='Error updating your profile')
    else:
        # user_form = UserModelForm(initial={
        #     'username': request.user.username,
        #     'email': request.user.email,
        # })
        # profile_form = ProfileModelForm(initial={
        #     'date_of_birth': request.user.profile.date_of_birth,
        #     'photo': request.user.profile.photo,
        # })
        user_form = UserModelForm(instance=user)
        profile_form = ProfileModelForm(instance=user.profile)
    ctx = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/edit.html', context=ctx)


# для смены пароля
class UpgradedPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('accounts:password_change_done')


# для восстановления пароля пароля
class UpgradedPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("accounts:password_reset_complete")


# для восстановления пароля пароля
class UpgradedPasswordResetView(PasswordResetView):
    success_url = reverse_lazy("accounts:password_reset_done")
