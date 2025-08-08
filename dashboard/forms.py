from django import forms
from .models import Account, Transaction


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
