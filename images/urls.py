from django.urls import path

from images.views import (
    create_image_view,
    detail_image_view,
    like_image_view,
    list_image_view,
    reset_likes_view,
    ranking_image_view,
)

app_name = 'images'

urlpatterns = [
    path('create/', create_image_view, name='create'),
    path('detail/<int:pk>/<slug:slug>/', detail_image_view, name='detail'),
    path('like/', like_image_view, name='like'),
    path('reset/', reset_likes_view, name='reset'),
    path('most-viewed/', ranking_image_view, name='ranking'),
    path('', list_image_view, name='list'),
]
