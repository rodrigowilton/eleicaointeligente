from django.db import models


class Candidato(models.Model):
	STATUS_CHOICES = [
		('A', 'Ativo'),
		('I', 'Inativo'),
	]

	nome = models.CharField(max_length=255)
	telefone = models.CharField(max_length=15)
	email = models.EmailField()
	usuario = models.CharField(max_length=50)
	senha = models.CharField(max_length=128)
	status = models.CharField(max_length=1, choices=STATUS_CHOICES)

	def __str__(self):
		return self.nome

class Meta(models.Model):
    meta_do_sistema = models.PositiveIntegerField(verbose_name='Meta do Sistema')
    controle_por_contato = models.PositiveIntegerField(verbose_name='Controle por Contato')

    def __str__(self):
        return f"Meta do Sistema: {self.meta_do_sistema}, Controle por Contato: {self.controle_por_contato}"