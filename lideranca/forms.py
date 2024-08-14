from django import forms
from .models import Lideranca, Contato
from candidato.models import StatusContato  # Importando o modelo Status

class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Usuário'}))
    senha = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))


class QRCodeForm(forms.Form):
    link = forms.ChoiceField(
        choices=[
            ('coordenador', 'Coordenador'),
            ('lideranca', 'Liderança'),
            ('contato', 'Contato')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class LiderancaForm(forms.ModelForm):
    class Meta:
        model = Lideranca
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
        }


class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'lideranca': forms.Select(attrs={'class': 'form-select'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'logradouro': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'uf': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control'}),
        }
    
    status = forms.ModelChoiceField(
        queryset=StatusContato.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    lideranca = forms.ModelChoiceField(
        queryset=Lideranca.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class RelatorioForm(forms.Form):
    data_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    data_fim = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    nome_lideranca = forms.ModelChoiceField(
        queryset=Lideranca.objects.all(),
        required=False,
        empty_label="Selecione uma liderança",
        widget=forms.Select(attrs={'class': 'form-control'})
    )