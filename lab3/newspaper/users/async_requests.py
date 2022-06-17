from asgiref.sync import sync_to_async

from .models import CustomUser
from articles.models import Article
from articles.views import logger


@sync_to_async
def get_articles_by_author(author):

    return Article.objects.filter(author=author)
