from django import forms

from .models import Answer, Question

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('body',)
        labels = {
            'body': '撰写答案',
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'body')
        labels = {
            'body': '问题描述(可选)',
        }