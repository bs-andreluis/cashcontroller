from django.db import models
from django.contrib.auth.models import User  # authentication system provided by django

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    name = models.CharField(max_length=100)  # Ex.: "Carteira Pessoal", "Investimentos"
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Saldo
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
    def calculate_balance(self):
        """
        Calcula o saldo atual baseado em receitas e gastos associados à carteira.
        """
        total_incomes = self.incomes.aggregate(total=models.Sum('amount'))['total'] or 0
        total_expenses = self.expenses.aggregate(total=models.Sum('amount'))['total'] or 0
        return total_incomes - total_expenses

class Expense(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="expenses")
    category = models.CharField(max_length=100)  # Categoria do gasto (ex.: "Alimentação")
    description = models.TextField(blank=True, null=True)  # Detalhes adicionais
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Valor do gasto
    date = models.DateField(auto_now_add=True)  # Data do gasto

    def __str__(self):
        return f"Gasto: {self.amount} - Categoria: {self.category} - Carteira: {self.wallet.name}"

 
class Income(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="incomes")
    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Valor da receita
    date = models.DateField(auto_now_add=True)  # Data da receita

    def __str__(self):
        return f"Receita: {self.amount} - Fonte: {self.source} - Carteira: {self.wallet.name}"


 