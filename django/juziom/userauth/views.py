# coding:utf8

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.models import User

from .form import LoginForm
from .models import UserProfile

def login(request):
    redirect_to = request.GET.get('next', '')
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response('users/login.html', RequestContext(request, {'form': form, }))
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                try:
                    userid=User.objects.get(username=username).id
                    UserProfile.objects.create(user_id=userid,level=10)
                except Exception:
                    print '已经有了'
                auth.login(request, user)
                if redirect_to:
                    return HttpResponseRedirect(redirect_to)
                else:
                    return HttpResponseRedirect('/')
            else:
                return render_to_response('users/login.html',
                                          RequestContext(request, {'form': form, 'password_is_wrong': True}))
        else:
            return render_to_response('users/login.html', RequestContext(request, {'form': form, }))


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/accounts/login/')
