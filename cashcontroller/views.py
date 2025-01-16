from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from cashcontroller import models
from cashcontroller.models import Wallet
from django.http.response import HttpResponse
from .models import Wallet, Expense, Income
from django.db.models import Sum

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

        Wallet.objects.create(
            user=my_user,
            balance=0.00  # Saldo inicial
        )

        return redirect('/entrar')
    return render(request, 'signup.html ')


def user_login(request):
    usuario = request.POST.get('usrnm')
    senha = request.POST.get('pswr')

    user = authenticate(username=usuario, password=senha)
    if user:
        login(request, user)
        return redirect('/carteira')
    else:
        print('senha/user invalido')

    return render(request, 'entrar.html')
    

def my_wallet(request):
     #if request.user.is_authenticated():
    try:
        wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        return render(request, 'error.html', {'message': 'Carteira não encontrada.'})
    
    total_incomes = wallet.incomes.aggregate(total=Sum('amount'))['total'] or 0.0
    total_expenses = wallet.expenses.aggregate(total=Sum('amount'))['total'] or 0.0
    balance = total_incomes - total_expenses
    info_cards = [
        {'title': 'INCOMES', 'value': f'R$ {total_incomes:.2f}', 'icon': 'bi bi-wallet2', 'color_class': 'bg-green'},
        {'title': 'OUTCOMES', 'value': f'R$ {total_expenses:.2f}', 'icon': 'bi bi-cash-stack', 'color_class': 'bg-red'},
        {'title': 'BALANCE', 'value': f'R$ {balance:.2f}', 'icon': 'bi bi-bar-chart-fill', 'color_class': 'bg-blue'},
    ]

    print(info_cards) 
    return render(request, 'dashboard.html', {'info_cards': info_cards})


def expenses(request):
    if request.method == 'POST':
        # Processar dados do formulário para criar uma nova despesa
        categoria = request.POST.get('ct')
        descricao = request.POST.get('dsc')
        data = request.POST.get('dt')
        valor = request.POST.get('vlr')

        # Obter a carteira do usuário logado
        try:
            carteira = Wallet.objects.get(user=request.user)
        except Wallet.DoesNotExist:
            return render(request, 'error.html', {'message': 'Carteira não encontrada.'})

        # Criar o novo gasto
        Expense.objects.create(
            wallet=carteira,
            amount=valor,
            category=categoria,
            description=descricao,
            date=data
        )

        # Redirecionar para evitar reenvio do formulário
        return redirect('expenses')  # Substitua 'expenses' pelo nome correto da URL, se necessário

    # Para requisições GET, apenas renderize o formulário
    return render(request, 'gastos.html')

    
def incomes (request):
    if request.method == 'POST':
        fonte = request.POST.get('ft')
        data = request.POST.get('dt')
        valor = request.POST.get('vlr')

        try:
            carteira = Wallet.objects.get(user=request.user)
        except Wallet.DoesNotExist:
            return render(request, 'error.html', {'message': 'Carteira não encontrada.'})

      
        Income.objects.create(
            wallet=carteira,
            source=fonte,
            amount=valor,
            date=data
        )

      
        return redirect('incomes')  

 
    return render(request, 'ganhos.html')
    