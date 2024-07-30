# coordenador/forms.py
from django import forms
from .models import Coordenador

class CoordenadorForm(forms.ModelForm):
    class Meta:
        model = Coordenador
        fields = [
            'nome', 'data_nascimento', 'sexo', 'cpf', 'nome_mae',
            'cep', 'logradouro', 'numero', 'complemento', 'bairro',
            'cidade', 'uf', 'email', 'telefone', 'usuario', 'senha'
        ]
        widgets = {
            'senha': forms.PasswordInput(),
        }
