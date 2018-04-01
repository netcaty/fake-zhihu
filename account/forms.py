from django import forms
from django.contrib.auth.models import User
from django.conf import settings

from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        ps1 = self.cleaned_data.get('password')
        ps2 = self.cleaned_data.get('password2')
        if ps1 and ps2 and ps1 != ps2:
            raise forms.ValidationError('密码不匹配')
        return self.cleaned_data

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        username = cleaned_data.get('username')
        if username:
            user = User.objects.filter(username=username)
            if user:
                raise forms.ValidationError('用户名已被占用')

        return cleaned_data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)