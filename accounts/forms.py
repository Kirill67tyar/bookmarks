from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, get_user_model

from images.utils import get_object_or_null

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        cd = self.cleaned_data
        username = cd.get('username')
        password = cd.get('password')
        user = get_object_or_null(User, username=username)
        if not user:
            raise forms.ValidationError('Такого пользователя не существует')
        if not check_password(password, user.password):
            raise forms.ValidationError('Пароль не правильный')
        if not user.is_active:
            raise forms.ValidationError('Пользователь не активный')
        return super().clean(*args, **kwargs)
