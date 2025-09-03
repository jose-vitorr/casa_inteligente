# Create your models here.
from django.db import models

class Casa(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome

class Comodo(models.Model):
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE, related_name='comodos')
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nome} ({self.casa.nome})'

class Dispositivo(models.Model):
    comodo = models.ForeignKey(Comodo, on_delete=models.CASCADE, related_name='dispositivos')
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    ligado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class Cena(models.Model):
    nome = models.CharField(max_length=100)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Acao(models.Model):
    cena = models.ForeignKey(Cena, on_delete=models.CASCADE, related_name='acoes')
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    ligar = models.BooleanField() # True para ligar, False para desligar
    ordem = models.PositiveIntegerField()
    intervalo_segundos = models.PositiveIntegerField(default=0, help_text="Intervalo em segundos ANTES de executar esta ação.")

    class Meta:
        ordering = ['ordem'] # Garante que as ações sejam ordenadas

    def __str__(self):
        acao = "Ligar" if self.ligar else "Desligar"
        return f'Ação {self.ordem}: {acao} {self.dispositivo.nome}'