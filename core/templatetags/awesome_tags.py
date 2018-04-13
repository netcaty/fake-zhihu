from django import template
from django.db.models import Count


from core.models import Question

register = template.Library()


@register.inclusion_tag('core/similar_questions.html')
def similar_questions(question):
    question_topics_ids = question.topics.values_list('id', flat=True)
    similar_questions = Question.objects.filter(topics__in=question_topics_ids) \
        .exclude(id=question.id)
    similar_questions = similar_questions.annotate(same_topics=Count('topics')) \
                            .order_by('-same_topics', '-created')[:5]

    return {'questions': similar_questions}


@register.inclusion_tag('core/form_errors.html')
def form_errors(form):
    errorlist = []
    for field, error in form.errors.items():
        errorlist.extend(error)

    return  {'errors': errorlist}