import datetime
import logging

from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser
from articles.models import Article
from .models import Comment

logger = logging.getLogger('main')


class CommentCreatePageTests(TestCase):

    def setUp(self) -> None:
        self.user = CustomUser.objects.create(
            username='username2',
            email='username2@gmail.com',
            password='12345678',
            age=22
        )
        self.article = Article.objects.create(
            title='title2',
            content='content2',
            date=datetime.datetime.now(),
            author=self.user
        )

    def test_comment_new_page_status_code_unauthenticated(self):
        response = self.client.post(reverse('comment_new', args=[str(self.article.pk)]), {
            'comment': 'comment2',
            'author': self.user,
            'article': self.article,
        })
        self.assertEqual(response.status_code, 302)

        self.assertTrue(reverse('login') in response.url)

    def test_comment_new_page_status_code_authenticated(self):
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('comment_new', args=[str(self.article.pk)]), {
            'comment': 'comment',
            'author': self.user,
            'article': self.article,
        })
        self.assertEqual(response.status_code, 302)  # get_success_url return /articles/ url

        self.assertTrue(reverse('article_list') in response.url)


class CommentEditPageTests(TestCase):

    def setUp(self) -> None:
        self.user = CustomUser.objects.create(
            username='username3',
            email='username3@gmail.com',
            password='654321',
            age=17
        )
        self.article = Article.objects.create(
            title='title3',
            content='content3',
            date=datetime.datetime.now(),
            author=self.user
        )
        self.comment = Comment.objects.create(
            comment='comment3',
            author=self.user,
            article=self.article
        )

    def test_comment_edit_page_status_code_unauthenticated(self):
        response = self.client.post(reverse('comment_edit', args=[str(self.article.pk), str(self.comment.pk)]), {
            'comment': 'comment(edited)'
        })
        self.assertEqual(response.status_code, 302)

        self.assertTrue(reverse('login') in response.url)

    def test_comment_edit_page_status_code_authenticated(self):
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('comment_edit', args=[str(self.article.pk), str(self.comment.pk)]), {
            'comment': 'comment(edited))'
        })
        self.assertEqual(response.status_code, 302)

        self.assertTrue(reverse('article_list') in response.url)


class CommentDeletePageTests(TestCase):

    def setUp(self) -> None:
        self.user = CustomUser.objects.create(
            username='username4',
            email='username4@gmail.com',
            password='87654321',
            age=16
        )
        self.article = Article.objects.create(
            title='title4',
            content='content4',
            date=datetime.datetime.now(),
            author=self.user
        )
        self.comment = Comment.objects.create(
            comment='comment4',
            author=self.user,
            article=self.article
        )

    def test_comment_delete_page_status_code_unauthenticated(self):
        response = self.client.get(reverse('comment_delete', args=[str(self.article.pk), str(self.comment.pk)]))
        self.assertEqual(response.status_code, 302)

        self.assertTrue(reverse('login') in response.url)

    def test_comment_delete_page_status_code_authenticated(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('comment_delete', args=[str(self.article.pk), str(self.comment.pk)]))
        self.assertEqual(response.status_code, 200)

    def test_template_used_by_comment_delete_page_authenticated(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('comment_delete', args=[str(self.article.pk), str(self.comment.pk)]))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'comments/comment_delete.html')
