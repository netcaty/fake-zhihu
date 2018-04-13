from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from taggit.managers import TaggableManager

class Question(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, related_name='questions')
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    topics = TaggableManager()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question_detail',
                       args=[self.id])

    def answers_count(self):
        return self.answers.count()


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers')
    author = models.ForeignKey(User, related_name='answers')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    body = models.TextField()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.body


class Action(models.Model):
    user = models.ForeignKey(User,
                             related_name='actions',
                             db_index=True)
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj')
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{self.user} {self.verb} {self.target} at {self.created}'.format(self=self)

    def get_target_model_name(self):
        return self.target_ct.model_class().__name__