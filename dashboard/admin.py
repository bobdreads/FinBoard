# Em dashboard/admin.py

from django.contrib import admin
from .models import Asset, Strategy, Tag, Operation, Movement, Attachment

# --- Customização do Admin para uma melhor experiência ---

# Isto permite editar 'Movimentações' e 'Anexos' DENTRO da página de uma 'Operação'
# É muito mais prático do que ter que criar cada um separadamente.


class MovementInline(admin.TabularInline):
    model = Movement
    extra = 0  # Mostra 1 campo extra para adicionar uma nova movimentação por padrão


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0  # Mostra 1 campo extra para um novo anexo


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    # ... (list_display, list_filter, etc. continuam iguais) ...
    list_display = ('id', 'user', 'asset', 'status',
                    'initial_operation_type', 'net_financial_result', 'start_date')
    list_filter = ('status', 'asset__market', 'strategy', 'user')
    search_fields = ('asset__ticker', 'user__username', 'strategy__name')
    inlines = [MovementInline, AttachmentInline]

    # Organiza os campos no formulário de edição para ficarem mais legíveis
    fieldsets = (
        ('Info Principal', {
            'fields': ('user', 'asset', 'status', 'initial_operation_type', 'strategy')
        }),

        # --- SEÇÃO ADICIONADA AQUI ---
        ('Plano de Trade', {
            'fields': ('initial_stop_price', 'initial_target_price')
        }),
        # --- FIM DA SEÇÃO NOVA ---

        ('Datas', {
            'fields': ('start_date', 'end_date')
        }),
        ('Análise e Resultado', {
            'fields': ('entry_reason', 'general_notes', 'entry_sentiment', 'execution_rating', 'tags')
        }),
        ('Resultados Calculados', {
            'fields': ('net_financial_result', 'points_pips_result')
        }),
    )


# Registrando os outros modelos de forma simples
admin.site.register(Asset)
admin.site.register(Strategy)
admin.site.register(Tag)
