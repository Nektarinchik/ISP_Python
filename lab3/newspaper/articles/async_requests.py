from asgiref.sync import sync_to_async

from .models import Article
from users.models import CustomUser


@sync_to_async
def get_all_authors():
    return CustomUser.objects.all()
