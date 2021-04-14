from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login

from login.models import User
from home.models import Substitution

def account(request):
    if request.user.is_authenticated:
        return render(request, 'account.html', {'user': request.user})
    else:
        return redirect('home')

def login_page(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('account')
        else:
            return render(request, 'login.html', {'incomplete_login': True})
    elif request.user.is_authenticated:
        logout(request)
        return redirect('home')
    else:
        return render(request, 'login.html', {'incomplete_login': False})

def inscription(request):
    if request.method == 'POST':
        if (
            request.POST['username'] != ''
            and request.POST['email'] != ''
            and request.POST['password'] != ''
        ):
            user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
            user.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, user)
            return redirect('account')
        else:
            return render(request, 'inscription.html', {"incomplete_inscription": True})
    return render(request, 'inscription.html', {"incomplete_inscription": False})