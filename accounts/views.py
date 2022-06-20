from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import (
    Paginator,
    PageNotAnInteger,
    EmptyPage
)
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
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

from accounts.models import Profile, Contact
from accounts.utils import anonymous_requeired
from accounts.forms import (
    LoginForm,
    UserModelForm,
    ProfileModelForm,
    UserRegistraionModelForm,
)

from actions.models import Action
from actions.utils import create_action
from common.decorators import ajax_required
from common.functions import is_ajax
from images.utils import (
    p_dir, p_mro, p_glob, p_loc, p_type,
    delimiter, p_content, show_builtins,
    show_doc, console_compose, get_object_or_null, console,
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
    user = request.user
    total_images_created = user.images_created.all().count()  # .related_name('images')
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
    actions = Action.objects.exclude(user=user).select_related('user',
                                                               'user__profile')  # SQL запрос будет в конце файла
    # в книге написано добавить в вычисление QS ещё prefetch_related('target')
    # но я проверил, что SQL запрос будет тот же
    following_ids = user.following.values_list('pk', flat=True)
    if following_ids:
        actions.filter(user_id__in=following_ids)
    paginator = Paginator(actions, 6)
    page_number = request.GET.get('page')
    try:
        actions = paginator.page(page_number)
    except PageNotAnInteger:
        actions = paginator.page(1)
    except EmptyPage:
        if is_ajax(request):
            return HttpResponse('')
        else:
            actions = paginator.page(paginator.num_pages)
    ctx = {
        'actions': actions,
        'section': 'dashboard',
        # 'total_images_created': total_images_created,
    }
    if is_ajax(request):
        template_name = 'actions/actions_list.html'
    else:
        template_name = 'accounts/dashboard.html'

    return render(
        request=request,
        template_name=template_name,
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
            create_action(
                user=new_user,
                verb='has created an account'
            )
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


@login_required
def list_user_view(request):
    object_list = User.objects.filter(is_active=True)
    ctx = {
        'object_list': object_list,
        'section': 'people',
    }
    return render(request, 'accounts/list.html', ctx)


@login_required
def detail_user_view(request, username):
    user = get_object_or_404(
        klass=User,
        username=username,
        is_active=True
    )
    count_followers = user.followers.filter(is_active=True).count()
    followers = user.followers.filter(is_active=True)
    ctx = {
        'user': user,
        'section': 'people',
        'count_followers': count_followers,
        'followers': followers,
    }
    return render(request, 'accounts/detail.html', ctx)


@ajax_required  # bad request (400)
@login_required  # bad request (400)
@require_POST  # HTTPResponseNotAllowed (405)
def follow_user_view(request):
    to_user_id = request.POST.get('id')
    action = request.POST.get('action')
    user = request.user
    if to_user_id and action:
        try:
            to_user = User.objects.get(pk=to_user_id)
            if action == 'follow':
                # создаём связь в таблице many to many
                Contact.objects.get_or_create(
                    from_user=user,
                    to_user=to_user
                )
                create_action(
                    user=user,
                    verb='is following',
                    target=to_user
                )
            else:
                # убираем связь в таблице many to many
                contact_instance = get_object_or_null(
                    model=Contact,
                    from_user=user,
                    to_user=to_user
                )
                # или
                # Contact.objects.filter(from_user=user, to_user=to_user).delete()
                if contact_instance:
                    contact_instance.delete()
        except User.DoesNotExist:
            pass
    return JsonResponse({'status': 'ok', })


# для смены пароля
class UpgradedPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('accounts:password_change_done')


# для восстановления пароля
class UpgradedPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("accounts:password_reset_complete")


# для восстановления пароля
class UpgradedPasswordResetView(PasswordResetView):
    success_url = reverse_lazy("accounts:password_reset_done")


# костыль для ngrok (туннелирование).
# почему-то через post запрос выдаёт ошибку с CSRF токеном
# поэтому это обработчик авторизации через get запрос
@anonymous_requeired
def login_through_get_view(request):
    username = request.GET.get('username')
    if username:
        form = LoginForm(request.GET)
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
    return render(request, 'accounts/login_through_get.html', {'form': form})


"""
SQL запрос для 
Action.objects.exclude(user=user).select_related('user', 'user__profile')

{'sql': 'SELECT "actions_action"."id", "actions_action"."user_id", '
        '"actions_action"."verb", "actions_action"."target_ct_id", '
        '"actions_action"."target_id", "actions_action"."created", '
        '"auth_user"."id", "auth_user"."password", "auth_user"."last_login", '
        '"auth_user"."is_superuser", "auth_user"."username", '
        '"auth_user"."first_name", "auth_user"."last_name", '
        '"auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", '
        '"auth_user"."date_joined", "accounts_profile"."id", '
        '"accounts_profile"."user_id", "accounts_profile"."date_of_birth", '
        '"accounts_profile"."photo" FROM "actions_action" INNER JOIN '
        '"auth_user" ON ("actions_action"."user_id" = "auth_user"."id") LEFT '
        'OUTER JOIN "accounts_profile" ON ("auth_user"."id" = '
        '"accounts_profile"."user_id") ORDER BY "actions_action"."created" '
        'DESC LIMIT 21',
 'time': '0.000'}

"""
