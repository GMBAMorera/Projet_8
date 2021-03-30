from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login

from login.models import User
from home.models import Substitution

def account(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return render(request, 'account.html', {
                'first_login': False,
                'user': user
            })
        elif (
            request.POST['username'] != ''
            and request.POST['email'] != ''
            and request.POST['password'] != ''
        ):
            user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
            user.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, user)
            return render(request, 'account.html', {
                'first_login': True,
                'user': user
            })
        else:
            return render(request, 'login.html', {'incomplete_login': True})
    else:
        if request.user.is_authenticated:
            return render(request, 'account.html', {
                'first_login': False,
                'user': request.user
            })
        else:
            return redirect('home')

def login_page(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')
    else:
        return render(request, 'login.html', {'incomplete_login': False})
