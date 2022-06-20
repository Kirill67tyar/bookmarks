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
from common.decorators import ajax_required


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
    return render(
        request=request,
        template_name='images/detail.html',
        context={
            'image': image,
            'total_likes': total_likes,
            'users_like': users_like,
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
