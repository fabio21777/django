from django.contrib import admin

from .models import Question
from .models import Choice

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text", "status"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

@admin.action(description="marca as questões selecionadas como publicadas")
def make_published(modeladmin, request, queryset):
    queryset.update(status="p")

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text", "status"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    # personalizando a exibição da lista de perguntas
    list_display = ["question_text", "pub_date", "was_published_recently", "status"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    actions = [make_published]





admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
