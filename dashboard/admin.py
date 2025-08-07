# Em dashboard/admin.py

from django.contrib import admin
# Não importamos mais nada do 'unfold'
from .models import Asset, Strategy, Tag, Operation, Movement, Attachment


class MovementInline(admin.TabularInline):
    model = Movement
    extra = 0


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):  # Garante que está usando admin.ModelAdmin
    list_display = ('id', 'user', 'asset', 'status',
                    'initial_operation_type', 'net_financial_result', 'start_date')
    list_filter = ('status', 'asset__market', 'strategy', 'user')
    search_fields = ('asset__ticker', 'user__username', 'strategy__name')
    inlines = [MovementInline, AttachmentInline]
    fieldsets = (
        ('Info Principal', {'fields': ('user', 'asset',
         'status', 'initial_operation_type', 'strategy')}),
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
