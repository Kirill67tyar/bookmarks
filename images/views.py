from redis import StrictRedis, exceptions

from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import (
    render,
    redirect,
    HttpResponse,
)
from django.core.paginator import (
    Paginator,
    PageNotAnInteger,
    EmptyPage,
)

from images.models import Image
from images.forms import ImageCreateModelForm
from images.utils import (
    get_object_or_null,
    is_ajax,
    console,
    p_dir,
)
from actions.utils import create_action
from common.decorators import (
    ajax_required,
    admin_required,
)

# создаём соединение с базой данных Redis
redis_db = StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)


@login_required
def create_image_view(request):
    if request.method == 'POST':
        form = ImageCreateModelForm(request.POST)
        if form.is_valid():
            image = form.save(commit=False)
            image.owner = request.user
            image.save()
            messages.success(request=request, message='Image successfully saved')
            create_action(
                user=request.user,
                verb='bookmarked image',
                target=image)
            return redirect(image.get_absolute_url())
        else:
            messages.success(request=request, message='Something went wrong (image not saved)')
    else:
        form = ImageCreateModelForm(request.GET)
    ctx = {
        'form': form,
        'action': 'images',
    }
    return render(
        request=request,
        template_name='images/create.html',
        context=ctx
    )


@login_required
def detail_image_view(request, pk, slug):
    user = request.user
    image = get_object_or_null(Image, pk=pk, slug=slug)

    # ----- console ------
    console(image.image.url)  # /media/images/2022/06/17/hz-kak-nazvat.jpg
    # ----- console ------

    total_likes = image.users_like.count()
    users_like = image.users_like.filter(is_active=True)

    # увеличивает ключ на один, и возвращает итоговое значение.
    # если ключа не было - создаёт его
    try:
        total_views = redis_db.incr(name=f'image:{image.pk}:views')
        redis_db.zincrby(
            name='image_ranking',  # название последовательности для ранжирования
            amount=1.,  # увеличиваем на 1.0
            value=image.pk  # что будет храниться в последовательности для ранжирования
        )
    except exceptions.ConnectionError:
        total_views = ''
    return render(
        request=request,
        template_name='images/detail.html',
        context={
            'image': image,
            'total_likes': total_likes,
            'users_like': users_like,
            'total_views': total_views,
            'user': user,
            'section': 'images',
        }
    )


@login_required
def list_image_view(request):
    images = Image.objects.all()
    paginator = Paginator(object_list=images,
                          per_page=8)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        if is_ajax(request):
            return HttpResponse('')
        page_obj = paginator.page(paginator.num_pages)
    ctx = {
        'page_obj': page_obj,
        'section': 'images',
    }
    if is_ajax(request):
        template_name = 'images/list_ajax.html',
    else:
        template_name = 'images/list.html',

    return render(
        request=request,
        template_name=template_name,
        context=ctx,
    )


@ajax_required  # bad request (400)
@require_POST  # HTTPResponseNotAllowed (405)
@login_required  # bad request (400)
def like_image_view(request):
    console(request.headers)
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    user = request.user
    if image_id and action:
        try:
            image = Image.objects.get(pk=image_id)
            if action == 'like':
                image.users_like.add(user)
                create_action(
                    user=user,
                    verb='likes',
                    target=image
                )
            else:
                image.users_like.remove(user)
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'ok', })


@login_required
def ranking_image_view(request):
    ranked_images = redis_db.zrange(
        name='image_ranking',  # имя последовтельности, куда сохраняем ранжированные id
        start=0,  # с первого индекса
        end=-1,  # до последнего (т.е. до конца)
        desc=True  # по убванию
    )
    ranked_images_ids = [int(i) for i in ranked_images]
    most_viewed_images = list(Image.objects.filter(
        pk__in=ranked_images_ids
    ))
    most_viewed_images.sort(
        key=lambda x: ranked_images_ids.index(x.pk)
    )
    return render(
        request=request,
        template_name='images/ranking.html',
        context={
            'most_viewed_images': most_viewed_images,
            'section': 'images',
        }
    )


@admin_required
def reset_likes_view(request):
    for image in Image.objects.all():
        image.total_likes = image.users_like.filter(is_active=True).count()
        image.save()
    return JsonResponse({'status': 'ok', })
