from django.urls import path
from django.contrib.auth import views as auth_views

from accounts.views import (
    edit_view,
    login_view,
    logout_view,
    register_view,
    dashboard_view,
    list_user_view,
    detail_user_view,
    follow_user_view,
    login_through_get_view,
    UpgradedPasswordChangeView,
    UpgradedPasswordResetView,
    UpgradedPasswordResetConfirmView,
)

app_name = 'accounts'

urlpatterns = [
    path('edit/', edit_view, name='edit'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('login-get/', login_through_get_view, name='login_through_get_view'),  # нужно для ngrok
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Read - list, detail
    path('users/', list_user_view, name='list_user'),
    path('users/follow/', follow_user_view, name='user_follow'),
    path('users/<str:username>/', detail_user_view, name='detail_user'),

    # для смены пароля
    path('password-change/', UpgradedPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # для восстановления пароля
    path('password-reset/', UpgradedPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', UpgradedPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # dashboard
    path('', dashboard_view, name='dashboard'),
]
