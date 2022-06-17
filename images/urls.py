from django.urls import path

from images.views import (
    create_image_view,
    detail_image_view,
)

app_name = 'images'

urlpatterns = [
    path('create/', create_image_view, name='create'),
    path('detail/<int:pk>/<slug:slug>/', detail_image_view, name='detail'),
]
