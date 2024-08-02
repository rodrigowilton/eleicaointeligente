from .models import Pesquisa
from django import forms
from .models import Prefeito, Vereador


class PrefeitoForm(forms.ModelForm):
	class Meta:
		model = Prefeito
		fields = ['nome']
		widgets = {
			'nome': forms.TextInput(attrs={'class': 'form-control'}),
		}


class VereadorForm(forms.ModelForm):
	class Meta:
		model = Vereador
		fields = ['nome']
		widgets = {
			'nome': forms.TextInput(attrs={'class': 'form-control'}),
		}


class PesquisaForm(forms.ModelForm):
	class Meta:
		model = Pesquisa
		fields = [
			'cidade', 'pesquisadora', 'bairro', 'sexo', 'idade',
			'indicacao_familia_brazao', 'voto_prefeito', 'voto_vereador',
			'rede_social', 'prioridade_prefeito', 'politico_impacto', 'voto_presidente'
		]

	# Adiciona uma opção 'Escolha' para cada campo de escolha
	SEXO_CHOICES = [('', 'Escolha'), ('masculino', 'Masculino'), ('feminino', 'Feminino')]
	idade = forms.ChoiceField(choices=[('', 'Escolha'), ('16 a 25 anos', '16 a 25 anos'),
									   ('26 a 34 anos', '26 a 34 anos'), ('35 a 55 anos', '35 a 55 anos'),
									   ('acima de 55 anos', 'Acima de 55 anos')])
	sexo = forms.ChoiceField(choices=SEXO_CHOICES)
	indicacao_familia_brazao = forms.ChoiceField(choices=[('', 'Escolha'), ('sim', 'Sim'), ('nao', 'Não')])
	voto_prefeito = forms.ChoiceField(choices=[('', 'Escolha')] + [(opcao, opcao) for opcao in
																   ['Candidato 1', 'Candidato 2', 'Candidato 3',
																	'Candidato 4', 'Candidato 5', 'Candidato 6']])
	voto_vereador = forms.ChoiceField(choices=[('', 'Escolha')] + [(opcao, opcao) for opcao in
																   ['Candidato 1', 'Candidato 2', 'Candidato 3',
																	'Candidato 4', 'Candidato 5', 'Candidato 6']])
	rede_social = forms.ChoiceField(
		choices=[('', 'Escolha'), ('facebook', 'Facebook'), ('whatsapp', 'WhatsApp'), ('instagram', 'Instagram'),
				 ('twitter', 'Twitter'), ('youtube', 'YouTube'), ('outros', 'Outros')])
	prioridade_prefeito = forms.ChoiceField(choices=[('', 'Escolha')] + [(opcao, opcao) for opcao in
																		 ['Saúde', 'Educação', 'Segurança',
																		  'Infraestrutura', 'Transporte', 'Habitação',
																		  'Meio Ambiente', 'Cultura', 'Economia',
																		  'Outros']])
	politico_impacto = forms.ChoiceField(choices=[('', 'Escolha')] + [(opcao, opcao) for opcao in
																	  ['Político 1', 'Político 2', 'Político 3',
																	   'Político 4', 'Político 5', 'Político 6']])
	voto_presidente = forms.ChoiceField(
		choices=[('', 'Escolha'), ('candidato_1', 'Candidato 1'), ('candidato_2', 'Candidato 2')])




