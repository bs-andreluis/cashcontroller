from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from cashcontroller.models import Wallet, Expense, Income


# Registro do modelo Wallet
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'balance', 'created_at', 'updated_at')  # Campos exibidos na lista
    search_fields = ('user__username', 'name')  # Permitir busca pelo nome do usuário ou nome da carteira
    list_filter = ('created_at',)  # Filtros laterais


# Personalizar o UserAdmin para incluir informações sobre carteiras
class CustomUserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'wallet_info')  # Adicionar coluna de informações da carteira

    def wallet_info(self, user):
        if hasattr(user, 'wallet'):  # Verifica se o usuário possui uma carteira
            return f"{user.wallet.name} - Saldo: {user.wallet.balance}"
        return "Sem carteira"
    wallet_info.short_description = "Carteira"


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'amount', 'category', 'date')
    search_fields = ('category', 'description')

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'amount', 'source', 'date')
    search_fields = ('source', 'description')