# coordenador/forms.py
from django import forms
from .models import Coordenador

class CoordenadorForm(forms.ModelForm):
    class Meta:
        model = Coordenador
        fields = [
            'nome', 'data_nascimento', 'sexo',
            'cep', 'logradouro', 'numero', 'complemento', 'bairro',
            'cidade', 'uf', 'email', 'telefone', 'usuario', 'senha'
        ]
        widgets = {
            'senha': forms.PasswordInput(),
        }

class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Usuário'}))
    senha = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))

