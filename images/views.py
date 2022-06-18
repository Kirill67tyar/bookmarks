from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import (
    render,
    redirect,
    HttpResponse,
)

from images.models import Image
from images.forms import ImageCreateModelForm
from images.utils import get_object_or_null, console
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
        }
    )


@ajax_required  # bad request (400)
@require_POST  # HTTPResponseNotAllowed (405)
@login_required  # bad request (400)
def like_image_view(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    user = request.user
    if image_id and action:
        try:
            image = Image.objects.get(pk=image_id)
            if action == 'like':
                image.users_like.add(user)
            else:
                image.users_like.remove(user)
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'ok', })
