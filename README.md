
desafio-dev-main
=========================

Descrição do projecto
O presente projecto é uma aplicação Django (previamente chamada de Desafio) que recebe do usuário um ficheiro .txt, faz o parseamento do mesmo e persiste os dados que encontrar dentro do mesmo ficheiro em um banco de dados.

Testato com Django 2.2.x e Python 3.x

#Observações:
-------------

Antes de mais agradecer pela oportunidade dada de poder participar neste processo e ter este teste. De facto pude investigar mais e aprender mais coisas que com certea fez toda a diferença na minha bagagem quanto programador.

Li o enunciado do desafio e fiquei mesmo muito entusiamado com os requerimentos, entretanto, infelizmente, alguns não foram concluídos. Propriamente: testes automatiados, docker e o end-point da API, por ainda não possuir conhecimentos profundos nessas áreas. Com certeza me serviu de alerta para que eu comece a estudar a componente prática aplicar estes conceitos, que por agora são apenas teóricos.

#Experiência de usuário
-------------

Ao usuário é apresentado a um formulário simples contendo campo para upload de ficheiros e um botão de submissão. Após o usuário seleccionar o ficheito (.txt com prévio tratamento) o código salva o ficheiro, faz o "parsamento" e periste os dados na tabela.
O resultado da operação de "parseamento" é exibida em formato de tabela numa págia seguinte.

O formulário permite apenas ficheiros .txt, com tratamento prévio, ou seja, deve ser feita uma distribuição dos dados a fim do algoritmo poder ender o significado de cada um dos valores e alocar este valor (individual) na posição correcta, para de depois persistir no banco de dados.

#Vamos lá!

Recursos:
-------------
code:: bash
	- Django = 2.2.4
	- Pillow

#Instalação
-------------
Instale o pacote executando:
code:: bash

	pip install Django=2.2.4
	
	and:
	pip install Pillow


O projecto Django possui uma única app "publicApp"

Em settings.py :

code:: python

    INSTALLED_APPS = (
                ...,
                'publicApp'
                )
                
O formato de hora foi alterado para UTC-3. Para isso, foi preciso mudar o TIME_ZONE padrão do projecto para:
    
code:: python
    TIME_ZONE = 'America/Belem'
    
Foi definida um caminho padrão para o upload dos files:
    code:: python
    MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'media/')
	MEDIA_URL = '/media/'

Em admin.py (publicApp):

code:: python
	from django.contrib import admin
	from .models import *
	
	admin.site.register(FileSubmit)
	admin.site.register(TipoTransacoes)
	admin.site.register(DocumentacaoCNAB)

Em models.py (publicApp):

O upload do ficheiro e a persistência do dados é feita em momentos diferentes. 
Primeiro é salvo o ficheiro.txt em um directório no servidor, depois faz-se referência a este último ficheiro salvo e sobre ele acontece as operações todas até se fazer a sumissão dos dados na tabela.

O constrangimento quanto ao tipo de ficheiro, foi imposto logo na base de dados, atraves do FileExtensionValidator e o valor padrão para data e hora UTC-3 foi possível atravez do timezone.now(), provindo do valor salvo em TIME_ZONE = 'America/Belem' em settings.py

code:: python
	from django.core.validators import FileExtensionValidator
	from django.forms.utils import from_current_timezone, timezone
	
	class FileSubmit(models.Model):
	    file = models.FileField(null=False, blank=False, validators=[FileExtensionValidator(allowed_extensions=['txt'])])
	    dataRegisto = models.DateTimeField(default=timezone.now)
	    
O projecto possui três models:

Onde são salvos os files.txt
code:: python
	FileSubmit()
	
Onde são salvos os tipos de transações. Devendo esta tabela ser preenchacida, antes das outras, por conta da chave estrangeira presente em Document DocumentacaoCNAB().
code:: python
	TipoTransacoes()

Devendo assim, se criar um superuser, atraves do comando
code:: python

	python3 manage.py createsuperuser

Após criar o superuser, siga para o browser https://127.0.0.1:8000/admin
faça o login e deverá preencher os valores da tabela com os seguintes valores:

| Tipo | Descrição | Natureza | Sinal |
| ---- | -------- | --------- | ----- |
| 1 | Débito | Entrada | + |
| 2 | Boleto | Saída | - |
| 3 | Financiamento | Saída | - |
| 4 | Crédito | Entrada | + |
| 5 | Recebimento Empréstimo | Entrada | + |
| 6 | Vendas | Entrada | + |
| 7 | Recebimento TED | Entrada | + |
| 8 | Recebimento DOC | Entrada | + |
| 9 | Aluguel | Saída | - |

sendo que o campo Natureza e Sinal serão tranformados em selects  cujo as opções estão armazenadas em variáveis globais com os respectivos nomes.

code:: python	
	DocumentacaoCNAB()

Na models DocumentacaoCNAB() é onde os dados parseados do file.txt são persistidos
   

#Em url.py (publicApp):

code:: python

	from django.conf.urls import url
	from .views import index, result

	urlpatterns = [
    	url(r'^$',index, name="index" ),
	    url(r'^result/(?P<pk>\w+)/$', result, name="result"),

	]
   	
#Em views.py (publicApp):

Conforme já havia frisado, a aplicação pertmite fazer o parseamento de um ficheiro .txt
code:: python

def index(request):
    fileURL = 0
    form = FileSubmitForm(request.POST or None, files=request.FILES)

    
    args = {
        'form':form,
        'fileURL':fileURL
        }
    return render(request, 'index.html', args)
    
#Documento bruto
|Valores brutos|
|----------------|
|3201903010000014200096206760174753****3153153453JOÃO MACEDO   BAR DO JOÃO       |
|5201903010000013200556418150633123****7687145607MARIA JOSEFINALOJA DO Ó - MATRIZ|
|3201903010000012200845152540736777****1313172712MARCOS PEREIRAMERCADO DA AVENIDA|
|2201903010000011200096206760173648****0099234234JOÃO MACEDO   BAR DO JOÃO       |
|1201903010000015200096206760171234****7890233000JOÃO MACEDO   BAR DO JOÃO   |

#Documento tratado:

| Tipo | Data | Valor | CPF | Cartão | Hora | Dono da loja | Nome da loja |
| ---- | -------- | --------- | -------- | ---------- | ------------ | -------------- | -------- |
|3| 2019-03-01| 000001420| 0096206760| 174753| 3153153453| JOÃO MACEDO| BAR DO JOÃO       |
|5| 2019-03-01| 000001320| 0556418150| 633123| 7687145607| MARIA JOSEFINA| LOJA DO Ó - MATRIZ |
|3| 2019-03-01| 000001220| 0845152540| 736777| 1313172712| MARCOS PEREIRA| MERCADO DA AVENIDA |
|2| 2019-03-01| 000001120| 0096206760| 173648| 0099234234| JOÃO MACEDO| BAR DO JOÃO       |

O documento foi submetido a um processo de tratamento a fim de separar os valores e assim submeter correctamente nos campos da tabela

Esta validação estrá presente no código python e o alerta no código html

code:: python
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

code:: html

	{% if messages %}
                  {% for message in messages %}
                  <div class="alter-danger">
                    <p><strong>{{message}} </strong></p>
                    <p>Não possui o tratamento prévio.</p>
                  </div>
                  {% endfor %}
	{% endif %}
