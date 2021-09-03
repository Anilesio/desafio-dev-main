from django.db import models
from django.core.validators import FileExtensionValidator
from django.forms.utils import from_current_timezone, timezone

# Create your models here.

class FileSubmit(models.Model):
    file = models.FileField(null=False, blank=False, validators=[FileExtensionValidator(allowed_extensions=['txt'])])
    dataRegisto = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.file.path

NATUREZA = (
    ('Entrada', 'Entrada'),
    ('Saída', 'Saída'),
)

SINAL = (
    ('+', '+'),
    ('-', '-'),
)

class TipoTransacoes(models.Model):
    descricao = models.CharField(max_length=100, null=False, blank=False, unique=True)
    natureza = models.CharField(max_length=20, null=True, blank=True, choices=NATUREZA, default="Entrada")
    sinal = models.CharField(max_length=20, null=True, blank=True, choices=SINAL, default="+")

    def __str__(self):
        return self.descricao

class DocumentacaoCNAB(models.Model):
    file = models.IntegerField(blank=True, null=True)
    tipo = models.ForeignKey(TipoTransacoes, null=True,blank=True, on_delete=models.CASCADE)
    data = models.DateTimeField(null=True, blank=True)
    valor = models.FloatField(null=True, blank=True)
    cpf = models.CharField(max_length=11, null=True, blank=True)
    cartao = models.IntegerField(null=True, blank=True)
    hora = models.CharField(null=True, blank=True, max_length=20)
    donoLoja = models.CharField(max_length=14, null=True, blank=True)
    nomeLoja = models.CharField(max_length=19, null=True, blank=True)

    def __str__(self):
        return self.nomeLoja
