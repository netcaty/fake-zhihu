from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse

from .forms import LoginForm, RegistrationForm, ProfileEditForm
from .models import Profile

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'],
                                password=data['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponse('帐号已被禁用')
            else:
                return HttpResponse('帐号或密码错误')

    else:
        form = LoginForm()
    return render(request, 'account/login.html',
                  {'form': form})

def register(request):
    if request.method == 'POST':
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.set_password(register_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        register_form = RegistrationForm()

    return render(request,
                  'account/register.html',
                  {'form': register_form})

def login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(username=data['username'],
                            password=data['password'])

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/')


    return render(request,
                  'registration/login.html',
                  {'form': form})
@login_required
def profile_edit(request):
    if request.method == 'POST':
        profile_form = ProfileEditForm(data=request.POST,files=request.FILES,
                                       instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, '资料更新成功')
            return HttpResponseRedirect(reverse('main:people', args=[request.user.username]))
        else:
            messages.error(request, '资料更新失败')
    else:
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,
                  'account/profile_edit.html',
                  {'profile_form': profile_form})