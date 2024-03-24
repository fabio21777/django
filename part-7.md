# Personalize o formulário do site de administração (https://docs.djangoproject.com/pt-br/5.0/intro/tutorial07/)

Ao registrarmos o modelo de Question``através da linha ``admin.site.register(Question), o Django constrói um formulário padrão para representá-lo. Comumente, você desejará personalizar a apresentação e o funcionamento dos formulários do site de administração do Django. Para isto, você precisará informar ao Django as opções que você quer utilizar ao registrar o seu modelo.

Vamos ver como isto funciona reordenando os campos no formulário de edição. Substitua a linha àdmin.site.register(Question)` por:

```python
from django.contrib import admin

from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]


admin.site.register(Question, QuestionAdmin)



## com fildset


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]

```


## Trabalhando com as alternativas e as questões

Aqui nos vamos exibir as alternativas de uma questão na mesma página que a questão em si. Para fazer isso, vamos adicionar uma classe ChoiceInline``ao QuestionAdmin``:

```python
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]

```

## Personalizando a página de listagem


```python
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    # personalizando a exibição da lista de perguntas
    list_display = ["question_text", "pub_date", "was_published_recently"]

	# Adicionar filtros
	list_filter = ["pub_date"]

	# Adicionar pesquisa
	search_fields = ["question_text"]




	## apara adicionar filtros é necessario uma modificação no model

	class Question(models.Model):
    question_text = models.CharField("Descrição da questão",max_length=200)
    pub_date = models.DateTimeField("data de publicação")

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

```

## Custimizando ações do admin

### importante

Rodar migrations para que as alterações sejam aplicadas

```bash
python manage.py makemigrations
python manage.py migrate
```


```python
## admin

@admin.action(description="marca as questões selecionadas como publicadas")
def make_published(modeladmin, request, queryset):
    queryset.update(status="p")

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]

    list_display = ["question_text", "pub_date", "was_published_recently"]
	list_filter = ["pub_date"]
	search_fields = ["question_text"]
	actions = [make_published]


```
