from django.contrib import admin

import comments.models
from . import models


class CommentInline(admin.TabularInline):
    model = comments.models.Comment


class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline
    ]


admin.site.register(models.Article, ArticleAdmin)
admin.site.register(comments.models.Comment)
