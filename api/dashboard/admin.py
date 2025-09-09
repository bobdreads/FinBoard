# api/dashboard/admin.py

from django.contrib import admin
from .models import (
    Portfolio,
    Strategy,
    Tag,
    Trade,
    TradeEntry,
    TradeStop,
    TradeTarget,
    TradeManualClose,
    JournalNote,
    PortfolioTransaction,
)

# --- Registos Personalizados com @admin.register ---


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'balance', 'currency')
    list_filter = ('user', 'currency')
    search_fields = ('name',)


@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)
    search_fields = ('name',)
    filter_horizontal = ('tags',)

# 1. AQUI ESTÁ A CORREÇÃO: Definimos as classes Inline PRIMEIRO


class TradeEntryInline(admin.TabularInline):
    model = TradeEntry
    extra = 1


class TradeTargetInline(admin.TabularInline):
    model = TradeTarget
    extra = 1


class TradeManualCloseInline(admin.TabularInline):
    model = TradeManualClose
    extra = 1

# 2. AGORA podemos usar as classes Inline aqui, pois elas já foram definidas


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'symbol', 'side', 'status',
                    'portfolio', 'user', 'net_result')
    list_filter = ('status', 'side', 'user', 'portfolio')
    search_fields = ('symbol',)
    inlines = [TradeEntryInline, TradeTargetInline, TradeManualCloseInline]


@admin.register(JournalNote)
class JournalNoteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'trade', 'strategy',
                    'confidence_level', 'created_at')
    list_filter = ('strategy', 'confidence_level', 'user')
    search_fields = ('notes', 'trade__symbol')
    autocomplete_fields = ('trade', 'strategy', 'user')


# --- Registos Simples para os outros modelos ---
# (O resto do ficheiro permanece igual)
admin.site.register(Tag)
admin.site.register(TradeEntry)
admin.site.register(TradeStop)
admin.site.register(TradeTarget)
admin.site.register(TradeManualClose)
admin.site.register(PortfolioTransaction)
