from django.urls import path
from django.contrib.auth import views as auth_views

from accounts.views import (
    login_view, logout_view, dashboard_view,
    MyPasswordChangeView,
)

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-change/', MyPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('', dashboard_view, name='dashboard'),
]
