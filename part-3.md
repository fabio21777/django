# Escrevendo sua primeira app Django, parte 3

Nesse capítulo, o foca será na criação de views no django

Escrevendo mais views¶
Agora vamos adicionar mais algumas views em polls/views.py. Estas views são um pouco diferentes, porque elas recebem um argumento

```python
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

```


criando rotas dinamicas

```python
from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
```

Dê uma olhada no seu navegador, em “/polls/34/”. Ele executará a detail() função e exibirá qualquer ID fornecido na URL. Experimente “/polls/34/results/” e “/polls/34/vote/” também – eles exibirão os resultados do espaço reservado e as páginas de votação.

Quando alguém solicita uma página do seu site – digamos, “/polls/34/”, o Django irá carregar o mysite.urlsmódulo Python porque ele é apontado pela ROOT_URLCONFconfiguração. Ele encontra a variável nomeada urlpatterns e percorre os padrões em ordem. Depois de encontrar a correspondência em 'polls/', ele remove o texto correspondente ( "polls/") e envia o texto restante – "34/"– para o URLconf 'polls.urls' para processamento posterior. Lá ele corresponde '<int:question_id>/', resultando em uma chamada para a detail()visualização assim

A parte question_id=34 vem de <int:question_id>. O uso de colchetes angulares “captura” parte da URL e a envia como um argumento de palavra-chave para a função de view. A parte question_id da string define o nome que será usado para identificar o padrão correspondente, e a parte int é um conversor que determina quais padrões devem corresponder a essa parte do caminho da URL. Os dois pontos (:) separam o conversor e o nome do padrão.


## Escreva views que façam algo

Cada view é responsável por fazer uma das duas coisas: devolver um objeto HttpResponse contendo o conteúdo para a página requisitada, ou levantar uma exceção como Http404. O resto é com você.

Sua view pode ler registros do banco de dados, ou não. Ela pode usar um sistema de templates como o do Django - ou outro sistema de templates Python de terceiros - ou não. Ele pode gerar um arquivo PDF, saída em um XML, criar um arquivo ZIP sob demanda, qualquer coisa que você quiser, usando qualquer biblioteca Python você quiser.

Tudo que o Django espera é que a view devolva um HttpResponse. Ou uma exceção.




Há um problema aqui, no entanto: o design da página esta codificado na view. Se você quiser mudar a forma de apresentação de sua página, você terá de editar este código diretamente em Python. Então vamos usar o sistema de templates do Django para separar o design do código Python:

Primeiro, crie um diretório chamado `` templates`` em seu diretório polls. O Django irá procurar templates lá.

A sua configuração de projeto TEMPLATES descreve como o Django vai carregar e renderizar templates. O arquivo de configuração padrão usa o backend DjangoTemplates do qual a opção APP_DIRS é configurada como True. Por convenção DjangoTemplates procura por um subdiretório “templates” em cada uma das INSTALLED_APPS.

Dentro do diretório templates que você acabou de criar, crie outro diretório chamado polls, e dentro dele crie um arquivo chamado index.html. Em outras palavras, seu template deve estar em polls/templates/polls/index.html. Por causa de como o carregador de template app_directories funciona conforme descrito acima, você pode se referir a este template dentro do Django como polls/index.html.


importante **
É um estilo muito comum usar get() e levantar uma exceção Http404 se o objeto não existir. O Django fornece um atalho para isso. Aqui esta a view detail(), reescrita:


Existe também a função get_list_or_404(), que trabalha da mesma forma que get_object_or_404() – com a diferença de que ela usa filter() ao invés de get(). Ela levanta Http404 se a lista estiver vazia.



Use o sistema de template


O sistema de templates usa uma sintaxe separada por pontos para acessar os atributos da variável. No exemplo de {{ question.question_text }}, primeiro o Django procura por dicionário no objeto question. Se isto falhar, ele tenta procurar por um atributo – que funciona, neste caso. Se a procura do atributo também falhar, ele irá tentar uma chamada do tipo list-index.

A chamada do método acontece no laço {% for %}: poll.choice_set.all é interpretado como código Python poll.choice_set.all(), que retorna objetos Choice iteráveis que são suportado para ser usado na tag {% for %}.

Veja o guia de templates para maiores detalhes sobre templates.


```html
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>

```


## Removendo URLs codificados nos templates
