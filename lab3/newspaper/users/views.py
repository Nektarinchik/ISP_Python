import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

import articles.models
import users.models
from . import forms
from articles.views import logger


class SignUpView(CreateView):
    logger.info('enter to SignUpView')
    form_class = forms.CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class AuthorArticlesListView(LoginRequiredMixin, ListView):
    logger.info('enter to AuthorArticlesListView')
    login_url = 'login'
    model = articles.models.Article
    template_name = 'users/author_articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        auth = users.models.CustomUser.objects.get(pk=self.kwargs['pk'])
        return articles.models.Article.objects.filter(author=auth)