"""
http://mysite.com:8000/create?title=nature&url=https://bipbap.ru/wp-content/uploads/2017/04/priroda_kartinki_foto_03.jpg
http://mysite.com:8000/create?title=road_with_moon&url=https://vjoy.cc/wp-content/uploads/2020/09/bezymyannyjkvytstsk.jpgрр



from django.http import HttpResponseBadRequest
HttpResponseBadRequest() - не ошибка (не унаследован он BaseException)
поэтому просто вызывается без raise
посылает HTTP-response с кододм ответа 400 (bad request)
"""
# from django.contrib.auth.models import User
#
# User
@login_required
def dashboard_view(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')
    paginator = Paginator(actions, 6)
    num_page = request.GET.get('page')
    try:
        actions = paginator.page(num_page)
    except PageNotAnInteger:
        actions = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        else:
            actions = paginator.page(paginator.num_pages)
    context = {
        'section': 'dashboard',
        'actions': actions,
    }
    if request.is_ajax():
        template_name = 'actions/action/actions_list.html'
    else:
        template_name = 'accounts/dashboard.html'
    return render(request, template_name=template_name, context=context)