from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, CreateView

import articles.models

from . import models
from articles.views import logger


class CommentEditView(LoginRequiredMixin, UpdateView):
    logger.info('enter to CommentEditView')
    login_url = 'login'
    model = models.Comment
    pk_url_kwarg = 'pk_c'
    fields = ['comment']
    template_name = 'comments/comment_edit.html'
    context_object_name = 'comment'


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    logger.info('enter to CommentDeleteView')
    login_url = 'login'
    model = models.Comment
    pk_url_kwarg = 'pk_c'
    template_name = 'comments/comment_delete.html'
    success_url = reverse_lazy('article_list')
    context_object_name = 'comment'


class CommentCreateView(LoginRequiredMixin, CreateView):
    logger.info('enter to CommentCreateView')
    login_url = 'login'
    model = models.Comment
    template_name = 'comments/comment_new.html'
    fields = ['comment']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.article = articles.models.Article.objects.get(id=self.kwargs['pk_a'])
        return super().form_valid(form)
