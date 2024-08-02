from django.db import models

class Lideranca(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    cpf = models.CharField(max_length=14)
    nome_mae = models.CharField(max_length=255)
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

class Contato(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    STATUS_CHOICES = [
        ('A', 'Ativo'),
        ('I', 'Inativo'),
    ]

    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    nome_mae = models.CharField(max_length=255)
    titulo = models.CharField(max_length=12)
    secao = models.CharField(max_length=10)
    local = models.CharField(max_length=255)
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    uf = models.CharField(max_length=2)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    observacao = models.TextField(blank=True, null=True)
    lideranca = models.ForeignKey(Lideranca, on_delete=models.CASCADE)
    msg = models.BooleanField(default=False)  # Campo para indicar se a mensagem foi enviada


    def __str__(self):
        return self.nome