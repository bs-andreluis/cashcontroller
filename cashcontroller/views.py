from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from cashcontroller import models
from cashcontroller.models import Wallet
from django.http.response import HttpResponse


def signup(request):
    if request.method == 'POST':
        usuario = request.POST.get('usrnm')
        email = request.POST.get('mail')
        senha = request.POST.get('pswr')
 
        ja_existe = User.objects.filter(username=usuario).first()
        if ja_existe:
            return HttpResponse ('Usuário já existe')
        
        my_user = User.objects.create_user(usuario,email,senha)
        my_user.save()
        return redirect('/entrar')
    return render(request, 'signup.html ')


def user_login(request):
    usuario = request.POST.get('usrnm')
    senha = request.POST.get('pswr')

    user = authenticate(username=usuario, password=senha)
    if user:
        login(request, user)
        return redirect('/wallet')
    else:
        print('senha/user invalido')

    return render(request, 'entrar.html')
    
def my_wallet(request):
    if request.user.is_authenticated():
        return render(request, 'wallet.html')