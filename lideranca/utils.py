from datetime import datetime
from .models import Lideranca, Contato
from django.db.models import Q


def aniversariantes_do_mes_atual_e_seguinte():
	"""Retorna uma lista de aniversariantes para o mês atual e o mês seguinte, sem considerar o ano."""
	hoje = datetime.now()
	mes_atual = hoje.month
	mes_seguinte = mes_atual + 1 if mes_atual < 12 else 1
	
	# Filtros para Lideranca
	liderancas = Lideranca.objects.filter(
		Q(data_nascimento__month=mes_atual) |
		Q(data_nascimento__month=mes_seguinte)
	)
	
	# Filtros para Contato
	contatos = Contato.objects.filter(
		Q(data_nascimento__month=mes_atual) |
		Q(data_nascimento__month=mes_seguinte)
	)
	
	return liderancas, contatos
