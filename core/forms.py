# Em core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """
    Formulário para o cadastro de novos usuários, agora com estilo!
    """
    # Adicionamos os campos que queremos além dos padrão (username, password1, password2)
    email = forms.EmailField(
        max_length=254, required=True, help_text='Obrigatório.')
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Opcional.')
    last_name = forms.CharField(
        max_length=150, required=False, help_text='Opcional.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Este é o truque: aplicamos um loop em todos os campos do formulário
        # e adicionamos a classe CSS a cada um deles.
        default_classes = "bg-gray-700 border border-gray-600 text-white text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full p-2.5"

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = default_classes
