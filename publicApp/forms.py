from django.forms import ModelForm
from django import forms
from .models import FileSubmit, DocumentacaoCNAB

class FileSubmitForm(forms.ModelForm):
    class Meta:
        model = FileSubmit
        fields = ['file']
class DocumentacaoCNABForm(forms.ModelForm):
    class Meta:
        model = DocumentacaoCNAB
        fields = ['tipo', 'valor', 'cpf', 'cartao', 'donoLoja', 'nomeLoja']
