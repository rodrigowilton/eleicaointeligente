from django import forms
from .models import Candidato
from .models import Meta


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
