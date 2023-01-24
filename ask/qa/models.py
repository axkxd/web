from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class QuestionManager(models.Manager):
    '''Менеджер для модели вопросов.'''
    def new(self):
        return self.order_by('-added_at')
    def popular(self):
        return self.order_by('-rating')


class Question(models.Model):
    '''Создает модель вопросов.'''
    title = models.CharField(max_length = 150)
    text = models.TextField(max_length = 1500)
    added_at = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(default = 0)
    objects = QuestionManager()

    author = models.ForeignKey(User, null = True, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name = 'likes')

    def get_url(self):
        return reverse('question', kwargs = {'id': self.id})

    def __unicode__(self) :
        return self.title


class Answer(models.Model):
    '''Создает модель ответов.'''
    text = models.TextField(max_length = 1500)
    added_at = models.DateTimeField(auto_now_add = True)

    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    author = models.ForeignKey(User, null = True, on_delete = models.CASCADE)