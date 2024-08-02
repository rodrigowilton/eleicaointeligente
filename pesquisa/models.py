from django.db import models

class Prefeito(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Vereador(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Pesquisa(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]

    IDADE_CHOICES = [
        ('16-25', '16 a 25 anos'),
        ('26-34', '26 a 34 anos'),
        ('35-55', '35 a 55 anos'),
        ('55+', 'Acima de 55 anos'),
    ]

    VOTARIA_CHOICES = [
        ('S', 'Sim'),
        ('N', 'Não'),
    ]

    REDES_SOCIAIS_CHOICES = [
        ('FB', 'Facebook'),
        ('WA', 'WhatsApp'),
        ('IG', 'Instagram'),
        ('TW', 'Twitter'),
        ('YT', 'YouTube'),
        ('OT', 'Outros'),
    ]

    cidade = models.CharField(max_length=100)
    pesquisadora = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    idade = models.CharField(max_length=5, choices=IDADE_CHOICES)
    votaria_brazao = models.CharField(max_length=1, choices=VOTARIA_CHOICES)
    prefeito = models.ForeignKey(Prefeito, on_delete=models.SET_NULL, null=True, related_name='pesquisas_prefeito')
    vereadores = models.ManyToManyField(Vereador, related_name='pesquisas_vereador')
    rede_social = models.CharField(max_length=2, choices=REDES_SOCIAIS_CHOICES)
    prioridade_prefeito = models.CharField(max_length=100)
    politico_mais_fez = models.CharField(max_length=100)
    votaria_presidente = models.CharField(max_length=1, choices=VOTARIA_CHOICES)

    def __str__(self):
        return f"Pesquisa {self.id} - {self.cidade}"
