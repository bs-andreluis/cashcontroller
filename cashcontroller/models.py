from django.db import models
from django.contrib.auth.models import User  # authentication system provided by django

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallets")
    name = models.CharField(max_length=100)  # Ex.: "Carteira Pessoal", "Investimentos"
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Saldo
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"
