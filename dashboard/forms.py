# Substitua todo o conteúdo de: bobdreads/finboard/FinBoard-4aa8007547cbb92200d5fbe4c83e75b99a1e9624/dashboard/forms.py

from django import forms
from .models import Account, Transaction, Operation, Asset, Strategy, Tag, Movement
from datetime import datetime

# --- WIDGET PERSONALIZADO PARA CORRIGIR O PROBLEMA DA DATA ---


class CustomDateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

    def format_value(self, value):
        # VERIFICA se o valor é um objeto datetime antes de formatar
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%dT%H:%M')
        # Se já for uma string (ao recarregar o form com erro), apenas a retorna
        return value

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

    # --- SUBSTITUA ESTE MÉTODO INTEIRO ---
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['account'].queryset = Account.objects.filter(user=user)

        # --- A CORREÇÃO ESTÁ AQUI ---
        # Tornamos os campos não-obrigatórios no formulário
        self.fields['start_date'].required = False
        self.fields['end_date'].required = False
        self.fields['status'].required = False

        # Escondemos os campos do usuário, pois são automáticos
        self.fields['start_date'].widget = forms.HiddenInput()
        self.fields['end_date'].widget = forms.HiddenInput()
        self.fields['status'].widget = forms.HiddenInput()

        # O resto da lógica permanece
        self.fields['net_financial_result'].required = False
        self.fields['points_pips_result'].required = False
        self.fields['general_notes'].required = False
        self.fields['execution_rating'].required = False

        # Aplica classes de estilo
        default_classes = "bg-gray-700 border border-gray-600 text-white text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5"
        for field_name, field in self.fields.items():
            # Ignora os campos ocultos que não precisam de estilo
            if not isinstance(field.widget, forms.HiddenInput):
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
