from django.db import models
from django.urls import reverse

import articles.models
from newspaper import settings


class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        to=articles.models.Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('article_list')
