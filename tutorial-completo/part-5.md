# part - 5

Felizmente, há um pequeno bug no pollsaplicativo para corrigirmos imediatamente: o Question.was_published_recently()método retorna Truese o Questionfoi publicado no último dia (o que é correto), mas também se o campo Questiondo pub_dateestá no futuro (o que certamente não é) .


O que aconteceu foi o seguinte:

manage.py test polls procurei testes no pollsaplicativo
encontrou uma subclasse da django.test.TestCaseclasse
criou um banco de dados especial para fins de teste
procurou métodos de teste - aqueles cujos nomes começam comtest
nele test_was_published_recently_with_future_questioncriou uma Question instância cujo pub_datecampo é 30 dias no futuro
… e usando o assertIs()método, descobriu que ele was_published_recently()retorna True, embora quiséssemos que ele retornasse False
O teste nos informa qual teste falhou e até mesmo a linha em que ocorreu a falha.

```python
def test_was_published_recently_with_old_question(self):
    """
    was_published_recently() returns False for questions whose pub_date
    is older than 1 day.
    """
    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
    old_question = Question(pub_date=time)
    self.assertIs(old_question.was_published_recently(), False)


def test_was_published_recently_with_recent_question(self):
    """
    was_published_recently() returns True for questions whose pub_date
    is within the last day.
    """
    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_question = Question(pub_date=time)
    self.assertIs(recent_question.was_published_recently(), True)
```

## testando a view

```python
def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )
```



Vejamos alguns deles mais de perto.

A primeira é uma função de atalho de pergunta, create_questionpara eliminar algumas repetições do processo de criação de perguntas.

test_no_questionsnão cria nenhuma pergunta, mas verifica a mensagem: “Nenhuma enquete está disponível”. e verifica se latest_question_listestá vazio. Observe que a django.test.TestCaseclasse fornece alguns métodos de asserção adicionais. Nestes exemplos, usamos assertContains()e assertQuerySetEqual().

Em test_past_question, criamos uma pergunta e verificamos se ela aparece na lista.

Em test_future_question, criamos uma pergunta com a pub_date no futuro. O banco de dados é redefinido para cada método de teste, portanto a primeira pergunta não está mais lá e, novamente, o índice não deve conter nenhuma pergunta.

E assim por diante. Na verdade, estamos usando os testes para contar uma história da entrada do administrador e da experiência do usuário no site, e verificando se em cada estado e para cada nova mudança no estado do sistema, os resultados esperados são publicados.
