from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import (
    Account, Transaction, Asset, Strategy, Tag,
    Operation, Movement, Attachment, Profile
)

# --- Registrando os Novos Modelos de Gestão de Capital ---


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Metas do Perfil'

# --- Define uma nova classe UserAdmin ---


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


# --- Re-registra o User admin ---
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'currency', 'initial_balance', 'is_active')
    list_filter = ('currency', 'is_active', 'user')
    search_fields = ('name',)
    # Adicionando a capacidade de editar transações diretamente da conta
    # inlines = [TransactionInline] # Descomente quando criarmos o Inline


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'type', 'amount', 'date')
    list_filter = ('type', 'account')
    autocomplete_fields = ['account']  # Facilita a busca por uma conta


# --- Configurações Anteriores (sem alterações) ---

class MovementInline(admin.TabularInline):
    model = Movement
    extra = 0


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'account', 'asset', 'status',
                    'net_financial_result', 'start_date')
    list_filter = ('status', 'account', 'asset__market', 'strategy', 'user')
    search_fields = ('asset__ticker', 'user__username',
                     'strategy__name', 'account__name')
    autocomplete_fields = ['account', 'asset', 'strategy', 'user', 'tags']
    inlines = [MovementInline, AttachmentInline]
    fieldsets = (
        ('Info Principal', {'fields': (
            'user', 'account', 'asset', 'status', 'initial_operation_type', 'strategy')}),
        ('Plano de Trade', {
         'fields': ('initial_stop_price', 'initial_target_price')}),
        ('Datas', {'fields': ('start_date', 'end_date')}),
        ('Análise e Resultado', {'fields': (
            'entry_reason', 'general_notes', 'entry_sentiment', 'execution_rating', 'tags')}),
        ('Resultados Calculados', {
         'fields': ('net_financial_result', 'points_pips_result')}),
    )


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    search_fields = ('ticker', 'name')
    list_filter = ('market', 'currency')


@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)
