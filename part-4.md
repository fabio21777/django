# cap 4
## Crie um formulário simples

```python
<form action="{% url 'polls:vote' question.id %}" method="post">
{% csrf_token %}
<fieldset>
    <legend><h1>{{ question.question_text }}</h1></legend>
    {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
    {% for choice in question.choice_set.all %}
        <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
        <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
    {% endfor %}
</fieldset>
<input type="submit" value="Vote">
</form>

```

```python
value="{{ choice.id }}"
```
A forma de vincular propriedade é relativamente comum as usadas em spas, mas aqui é um pouco diferente. O valor do atributo name é a chave que será enviada para o servidor quando o formulário for submetido. O valor do atributo value é o valor que será enviado para o servidor se este botão de rádio for selecionado. O atributo id é usado para identificar o botão


Uma rápida explicação:

* O template acima exibe um botão radio para cada opção da enquete. O value de cada botão radio está associado ao ID da opção. O name de cada botão radio é a escolha "choice". Isso significa que, quando alguém escolhe um dos botões de radio e submete a formulário, ele vai enviar o dado``choice=#`` por POST onde # é o ID da escolha selecionada. Este é o conceito básico sobre formulários HTML.

* Definimos o formulário actioncomo e definimos . Usar (em oposição a ) é muito importante, porque o ato de enviar este formulário alterará os dados do lado do servidor. Sempre que você criar um formulário que altere os dados do lado do servidor, use . Esta dica não é específica do Django; é uma boa prática de desenvolvimento web em geral.{% url 'polls:vote' question.id %}method="post"method="post"method="get"method="post"


* forloop.counter indica quantas vezes a tag :ttag`for` passou pelo laço.


* Como estamos criando um formulário POST (que pode ter o efeito de modificar dados), precisamos nos preocupar com falsificações de solicitações entre sites. Felizmente, você não precisa se preocupar muito, porque o Django vem com um sistema útil para se proteger contra isso. Resumindo, todos os formulários POST direcionados a URLs internos devem usar a tag template.{% csrf_token %}

```python
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question


# ...
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
```
descrição do codigo acima

request.POST é um objeto como dicionários que lhe permite acessar os dados submetidos pelos seus nomes chaves. Neste caso, request.POST['choice'] retorna o ID da opção selecionada, como uma string. Os valores de request.POST são sempre strings.

Note que Django também fornece request.GET para acesar dados GET da mesma forma – mas nós estamos usando attr:request.POST <django.http.HttpRequest.POST> explicitamente no nosso código, para garantir que os dados só podem ser alterados por meio de uma chamada POST.

request.POST['choice'] irá levantar a exceção KeyError caso uma choice não seja fornecida via dados POST. O código acima checa por KeyError e re-exibe o formulário da enquete com as mensagens de erro se uma choice não for fornecida.

F("votes") + 1 instrui o banco de dados a aumentar a contagem de votos em 1.

Após incrementar uma opção, o código retorna um class:~django.http.HttpResponseRedirect em vez de um normal HttpResponse. HttpResponseRedirect` recebe um único argumento: a URL para o qual o usuário será redirecionado (veja o ponto seguinte para saber como construímos a URL, neste caso).

Como o comentário do Python acima aponta, você deve sempre retornar an HttpResponseRedirectdepois de lidar com sucesso com os dados POST. Esta dica não é específica do Django; é uma boa prática de desenvolvimento web em geral.

Estamos usando a função reverse() no construtor da HttpResponseRedirect neste exemplo. Essa função nos ajuda a evitar de colocar a URL dentro da view de maneira literal. A ele é dado então o nome da “view” que queremos que ele passe o controle e a parte variável do padrão de formato da URL que aponta para a “view”. Neste caso, usando o URLconf nós definimos em Tutorial 3, esta chamada de reverse() irá retornar uma string como
