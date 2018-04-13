from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.contrib import messages

from taggit.models import Tag

from redis import StrictRedis, ConnectionPool

from account.models import Contact
from .models import Question, Action
from .forms import AnswerForm, QuestionForm
from .utils import create_action
from .decorators import ajax_required

pool = ConnectionPool(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)
r = StrictRedis(connection_pool=pool)


@login_required
def activity(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids) \
            .select_related('user', 'user__profile') \
            .prefetch_related('target')

    return render(request,
                  'core/activity.html',
                  {'actions': actions})


@login_required
def question(request):
    questions = Question.objects.all()

    return render(request,
                  'core/question.html',
                  {'questions': questions})


@login_required
def question_ranking(request):
    question_ranking = r.zrange('question_ranking', 0, -1,
                                desc=True)[:10]
    question_ranking_ids = [int(id) for id in question_ranking]
    most_viewd = list(Question.objects.filter(id__in=question_ranking_ids))
    most_viewd.sort(key=lambda x: question_ranking_ids.index(x.id))

    return render(request,
                  'core/question_rank.html',
                  {'most_viewd': most_viewd})


# 首页视图转到这里
index = question


def question_detail(request, id):
    question = get_object_or_404(Question, pk=id)
    answers = question.answers.all()
    # total_views = r.incr('question:{}:views'.format(question.id))
    # r.zincrby('question_ranking', question.id, 1)

    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if question.answers.filter(author=request.user).exists():
            messages.error(request, '你已回答过此问题了！')
            return redirect(question)
        if answer_form.is_valid():
            new_answer = answer_form.save(commit=False)
            new_answer.question = question
            new_answer.author = request.user
            new_answer.save()
            create_action(request.user, '回答了问题', question)
            messages.success(request, '你已成功回答此问题!')
            return redirect(question)
    else:
        answer_form = AnswerForm()
    return render(request,
                  'core/question_detail.html',
                  {'question': question,
                   'answers': answers,
                   'answer_form': answer_form})


@login_required
def topic(request):
    topics = Tag.objects.all()
    return render(request,
                  'core/topics.html',
                  {'topics': topics})


def people(request, username):
    user = get_object_or_404(User, username=username)
    actions = Action.objects.filter(user=user)
    return render(request,
                  'core/people.html',
                  {'user': user, 'actions': actions})


@login_required
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.author = request.user
            new_question.save()
            messages.success(request, '你问了一个问题')
            return redirect(reverse('question'))
    else:
        form = QuestionForm()

    return render(request, 'core/ask.html',
                  {
                      'form': form
                  })


@require_POST
@ajax_required
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(pk=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
                create_action(request.user, '关注了用户', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})


def search(request):
    word = request.GET.get('word')
    if not word:
        return JsonResponse({'error': 'You got nothing'})
    return JsonResponse({'success': 'Will be complete soon!'})
