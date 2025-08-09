from django import forms
from .models import Account, Transaction, Operation, Asset, Strategy, Tag, Movement


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        # Excluímos o usuário, pois ele será preenchido automaticamente pela view
        fields = ['name', 'currency', 'initial_balance', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicando as classes do TailwindCSS para um visual consistente
        default_classes = "bg-gray-700 border border-gray-600 text-white text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5"
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                # Estilo diferente para checkboxes
                field.widget.attrs['class'] = "w-4 h-4 text-indigo-600 bg-gray-700 border-gray-600 rounded focus:ring-indigo-500"
            else:
                field.widget.attrs['class'] = default_classes


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        # O campo 'account' será preenchido pela view, não pelo usuário
        fields = ['type', 'amount', 'date', 'description']
        # Usamos um widget para o campo de data para ter um seletor de data/hora amigável
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicando as classes do TailwindCSS
        default_classes = "bg-gray-700 border border-gray-600 text-white text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5"
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = default_classes


class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = [
            'account', 'asset', 'strategy', 'initial_operation_type',
            'initial_stop_price', 'initial_target_price',
            'net_financial_result', 'points_pips_result',
            'entry_reason', 'general_notes', 'entry_sentiment', 'execution_rating',
            'tags'
        ]
        widgets = {
            # REMOVA os widgets do select2
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'entry_reason': forms.Textarea(attrs={'rows': 4}),
            'general_notes': forms.Textarea(attrs={'rows': 4}),
            # O widget de tags pode ser o padrão ou um customizado
            'tags': forms.SelectMultiple(attrs={'class': 'h-40'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['account'].queryset = Account.objects.filter(user=user)

        self.fields['net_financial_result'].required = False
        self.fields['points_pips_result'].required = False
        self.fields['general_notes'].required = False
        self.fields['execution_rating'].required = False

        # Aplica classes para todos os campos
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


class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ['type', 'datetime', 'quantity', 'price', 'costs']
        widgets = {
            'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_classes = "bg-gray-700 border border-gray-600 text-white text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5"
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = default_classes
