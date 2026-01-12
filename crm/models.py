from django.db import models
from django.conf import settings

class Empresa(models.Model):
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    setor = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nome

class Contato(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='contatos')
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nome

class Oportunidade(models.Model):
    ESTAGIOS = [
        ('novo', 'Novo'),
        ('qualificado', 'Qualificado'),
        ('proposta', 'Proposta'),
        ('negociacao', 'Negociação'),
        ('ganho', 'Ganho'),
        ('perdido', 'Perdido'),
    ]

    titulo = models.CharField(max_length=255)
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    estagio = models.CharField(max_length=20, choices=ESTAGIOS, default='novo')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} ({self.contato.nome})"