from django.shortcuts import render
from .forms import FileSubmitForm
from .models import FileSubmit, DocumentacaoCNAB, TipoTransacoes
from django.shortcuts import render, HttpResponseRedirect, reverse
import os.path
import datetime
from django.contrib import messages
# Create your views here.

def index(request):
    fileURL = 0
    form = FileSubmitForm(request.POST or None, files=request.FILES)

    try:
        if form.is_valid():
            formCommit = form.save(commit=False)
            formCommit.save()
            fileURL = FileSubmit.objects.get(id = int(formCommit.id))

            list = []
            with open(str(fileURL.file.path), 'r') as arquivo:
                for valor in arquivo:
                    list.append(valor.split(','))

                for l in list:
                    doc = DocumentacaoCNAB()
                    objecto = TipoTransacoes.objects.get(id = int(l[0]))
                    doc.tipo = objecto
                    doc.data = datetime.datetime.strptime(l[1].strip(), '%Y-%m-%d')
                    doc.valor = float(l[2]) / 100
                    doc.cpf = l[3]
                    doc.cartao = l[4]
                    doc.hora = l[5]
                    doc.donoLoja = l[6]
                    doc.nomeLoja = l[7]
                    doc.file = formCommit.id
                    doc.save()
                    print(l)
            messages.success(request, "Sucesso! Ficheiro parseado.")
            return HttpResponseRedirect(reverse('publicApp:result', kwargs={'pk':int(formCommit.id)}))
    except:
            messages.success(request, "O ficheiro não está de acordo com o formato esperado.")
            return HttpResponseRedirect(reverse('publicApp:index'))
    args = {
        'form':form,
        'fileURL':fileURL
        }
    return render(request, 'index.html', args)

def result(request, pk):
    idFile = FileSubmit.objects.get(id = int(pk))
    objectos = DocumentacaoCNAB.objects.all().filter(file = idFile.id)
    args = {
        'objectos':objectos,
        'total':objectos.count(),
        'idFile':idFile
    }
    return render(request, 'result.html', args)
