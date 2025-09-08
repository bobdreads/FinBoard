# api/dashboard/admin.py

from django.contrib import admin
# 1. Importamos os NOSSOS NOVOS modelos
from .models import (
    Portfolio,
    Strategy,
    Trade,
    TradeEntry,
    TradeStop,
    TradeTarget,
    TradeManualClose,
    JournalNote,
    PortfolioTransaction,
)

# 2. Registamos cada novo modelo para que apareça no painel de admin.
#    Isto permite-nos criar, ver, editar e apagar dados facilmente.


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'balance', 'currency', 'created_at')
    list_filter = ('user', 'currency')
    search_fields = ('name',)


@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)
    search_fields = ('name',)

# Para o Trade, podemos mostrar as suas entradas e saídas diretamente na página de detalhes


class TradeEntryInline(admin.TabularInline):
    model = TradeEntry
    extra = 1  # Começa com 1 campo extra para adicionar uma nova entrada


class TradeTargetInline(admin.TabularInline):
    model = TradeTarget
    extra = 1


class TradeManualCloseInline(admin.TabularInline):
    model = TradeManualClose
    extra = 1


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'symbol', 'side', 'portfolio',
                    'user', 'is_open', 'net_result')
    list_filter = ('is_open', 'side', 'user', 'portfolio')
    search_fields = ('symbol',)
    # Adicionamos os Inlines para uma gestão mais fácil
    inlines = [TradeEntryInline, TradeTargetInline, TradeManualCloseInline]


@admin.register(JournalNote)
class JournalNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'trade', 'strategy',
                    'confidence_level', 'created_at')
    list_filter = ('strategy', 'confidence_level')


@admin.register(PortfolioTransaction)
class PortfolioTransactionAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'type', 'value', 'date')
    list_filter = ('type', 'portfolio')


# Também podemos registar os outros modelos se quisermos editá-los individualmente
admin.site.register(TradeEntry)
admin.site.register(TradeStop)
admin.site.register(TradeTarget)
admin.site.register(TradeManualClose)
