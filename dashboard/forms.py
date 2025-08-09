# Substitua todo o conteúdo de: bobdreads/finboard/FinBoard-4aa8007547cbb92200d5fbe4c83e75b99a1e9624/dashboard/forms.py

from django import forms
from .models import Account, Transaction, Operation, Asset, Strategy, Tag, Movement

# --- WIDGET PERSONALIZADO PARA CORRIGIR O PROBLEMA DA DATA ---


class CustomDateTimeInput(forms.DateTimeInput):
    """Widget para formatar a data/hora para o input datetime-local do HTML."""
    input_type = 'datetime-local'

    def format_value(self, value):
        if value:
            # O 'T' é o separador que o HTML exige
            return value.strftime('%Y-%m-%dT%H:%M')
        return None

# --- FORMULÁRIOS DA APLICAÇÃO ---


class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        # INCLUÍMOS TODOS OS CAMPOS PARA QUE O FORMULÁRIO POSSA MANIPULÁ-LOS
        fields = [
            'start_date', 'end_date', 'status', 'account', 'asset', 'strategy',
            'initial_operation_type', 'initial_stop_price', 'initial_target_price',
            'net_financial_result', 'points_pips_result', 'entry_reason',
            'general_notes', 'entry_sentiment', 'execution_rating', 'tags'
        ]
        # APLICAMOS O WIDGET CORRETO AOS CAMPOS DE DATA
        widgets = {
            'start_date': CustomDateTimeInput(),
            'end_date': CustomDateTimeInput(),
            'entry_reason': forms.Textarea(attrs={'rows': 4}),
            'general_notes': forms.Textarea(attrs={'rows': 4}),
            'tags': forms.SelectMultiple(attrs={'class': 'h-40'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['account'].queryset = Account.objects.filter(user=user)

        # TORNAMOS OS CAMPOS AUTOMÁTICOS APENAS LEITURA (DISABLED)
        # Como eles estão na lista 'fields', esta operação agora é segura.
        self.fields['start_date'].disabled = True
        self.fields['end_date'].disabled = True
        self.fields['status'].disabled = True

        # Campos opcionais
        self.fields['net_financial_result'].required = False
        self.fields['points_pips_result'].required = False
        self.fields['general_notes'].required = False
        self.fields['execution_rating'].required = False

        # Aplica classes de estilo
        default_classes = "bg-gray-700 border border-gray-600 text-white text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5"
        disabled_classes = "bg-gray-800 border-gray-700 text-gray-400 text-sm rounded-lg block w-full p-2.5 cursor-not-allowed"

        for field_name, field in self.fields.items():
            if field.disabled:
                field.widget.attrs['class'] = disabled_classes
            else:
                field.widget.attrs['class'] = default_classes


class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ['type', 'datetime', 'quantity', 'price', 'costs']
        widgets = {
            # GARANTE QUE O WIDGET CORRETO SEJA USADO AQUI TAMBÉM
            'datetime': CustomDateTimeInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_classes = "bg-gray-700 border border-gray-600 text-white text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5"
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = default_classes


class StrategyForm(forms.ModelForm):
    class Meta:
        model = Strategy
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_classes = "bg-gray-700 border border-gray-600 text-white text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5"
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = default_classes

# Adicionando o AccountForm e TransactionForm que já tínhamos para manter o arquivo completo


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'currency', 'initial_balance', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_classes = "bg-gray-700 border border-gray-600 text-white text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5"
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = "w-4 h-4 text-indigo-600 bg-gray-700 border-gray-600 rounded focus:ring-indigo-500"
            else:
                field.widget.attrs['class'] = default_classes


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'amount', 'date', 'description']
        widgets = {
            'date': CustomDateTimeInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_classes = "bg-gray-700 border border-gray-600 text-white text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5"
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = default_classes
