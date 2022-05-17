import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView

from . import models

logger = logging.getLogger('main')


class ArticleListView(LoginRequiredMixin, ListView):
    logger.info('enter to ArticleListView')
    login_url = 'login'
    template_name = 'articles/article_list.html'
    model = models.Article
    context_object_name = 'articles'


class ArticleDetailView(LoginRequiredMixin, DetailView):
    logger.info('enter to ArticleDetailView')
    login_url = 'login'
    model = models.Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    logger.info('enter to ArticleUpdateView')
    login_url = 'login'
    model = models.Article
    fields = ['title', 'content']
    template_name = 'articles/article_edit.html'
    context_object_name = 'article'


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    logger.info('enter to ArticleDeleteView')
    login_url = 'login'
    model = models.Article
    template_name = 'articles/article_delete.html'
    success_url = reverse_lazy('article_list')
    context_object_name = 'article'


class ArticleCreateView(LoginRequiredMixin, CreateView):
    logger.info('enter to ArticleCreateView')
    login_url = 'login'
    model = models.Article
    template_name = 'articles/article_new.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
