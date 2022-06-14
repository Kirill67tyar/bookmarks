from django.urls import path
from django.contrib.auth import views as auth_views

from accounts.views import (
    edit_view,
    login_view,
    logout_view,
    register_view,
    dashboard_view,
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

    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),

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
