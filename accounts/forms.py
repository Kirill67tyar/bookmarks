from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, get_user_model

from accounts.models import Profile
from images.utils import get_object_or_null

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        cd = self.cleaned_data
        username = cd.get('username')
        password = cd.get('password')
        user = get_object_or_null(User, username=username) or get_object_or_null(User, email=username)
        if not user:
            raise forms.ValidationError('Такого пользователя не существует')
        if not check_password(password, user.password):
            raise forms.ValidationError('Пароль не правильный')
        if not user.is_active:
            raise forms.ValidationError('Пользователь не активный')
        return super().clean(*args, **kwargs)


class UserRegistraionModelForm(forms.ModelForm):
    password = forms.CharField(
        label='Enter password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username', 'email',)
        widgets = {
            'email': forms.EmailInput,
        }

    def clean_password2(self):
        cd = self.cleaned_data
        password = cd.get('password')
        password2 = cd.get('password2')
        if password != password2:
            raise forms.ValidationError("Password didn't match")
        return password2


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = 'date_of_birth', 'photo',
        widgets = {
            'date_of_birth': forms.DateInput,
        }


class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = 'username', 'email',
