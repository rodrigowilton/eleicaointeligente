from django import forms
from .models import Candidato
from .models import Meta
from .models import StatusContato

class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Usuário'}))
    senha = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))


class CandidatoForm(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = ['nome', 'telefone', 'email', 'usuario', 'senha', 'status']
        widgets = {
            'senha': forms.PasswordInput(),  # Oculta a senha no formulário
        }

class MetaForm(forms.ModelForm):
    class Meta:
        model = Meta
        fields = ['meta_do_sistema', 'controle_por_contato']


class StatusForm(forms.ModelForm):
    class Meta:
        model = StatusContato
        fields = ['status_do_contato']


