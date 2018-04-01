from django.contrib import admin

# Register your models here.
from .models import Question, Answer, Action

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'created', 'updated')
    list_filter = ('created', 'updated', 'author')
    search_fields = ('title', 'body')
    ordering = ['title']

admin.site.register(Question, QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'body', 'author', 'created', 'updated')
    list_filter = ('author',)
    search_fields = ('body',)
    ordering = ['created']

admin.site.register(Answer, AnswerAdmin)

class ActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'verb', 'target', 'created')
    list_filter = ('created',)
    search_fields = ('verb',)

admin.site.register(Action, ActionAdmin)