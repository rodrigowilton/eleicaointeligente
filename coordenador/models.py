from django.db import models

class Coordenador(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    uf = models.CharField(max_length=2)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    usuario = models.CharField(max_length=150)
    senha = models.CharField(max_length=128)

    def __str__(self):
        return self.nome
