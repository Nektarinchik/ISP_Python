import datetime
import logging
import re

from django.test import TestCase
from django.urls import reverse

from .models import Article
from comments.models import Comment
from users.models import CustomUser

logger = logging.getLogger('main')


class ArticleCreatePageTests(TestCase):

    def setUp(self) -> None:
        self.user = CustomUser.objects.create(
            username='username5',
            email='username5@gmail.com',
            password='123456',
            age=10
        )
        self.article = Article.objects.create(
            title='title5',
            content='content5',
            date=datetime.datetime.now(),
            author=self.user
        )
        self.comment = Comment.objects.create(
            comment='comment5',
            author=self.user,
            article=self.article
        )

    def test_article_create_page_status_code_unauthenticated(self):
        response = self.client.post(reverse('article_new'), {
            'title': 'test_title',
            'content': 'test_content'
        })
        self.assertEqual(response.status_code, 302)

        self.assertTrue(reverse('login') in response.url)

    def test_article_create_page_status_code_authenticated(self):
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('article_new'), {
            'title': 'test_title',
            'content': 'test_content'
        })
        self.assertEqual(response.status_code, 302)

        url_pattern = re.compile(r'/articles/\d+/')
        self.assertTrue(re.match(url_pattern, response.url) is not None)


class ArticleListPageTests(TestCase):

    def setUp(self) -> None:
        self.user = CustomUser.objects.create(
            username='username6',
            email='username6@gmail.com',
            password='123456',
            age=10
        )
        self.article = Article.objects.create(
            title='title6',
            content='content6',
            date=datetime.datetime.now(),
            author=self.user
        )
        self.comment = Comment.objects.create(
            comment='comment6',
            author=self.user,
            article=self.article
        )

    def test_article_list_page_status_code_unauthenticated(self):
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 302)

        self.assertTrue(reverse('login') in response.url)

    def test_article_list_page_status_code_authenticated(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)

    def test_template_used_by_article_list_page_authenticated(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'articles/article_list.html')

        self.assertContains(response, 'username6')
        self.assertContains(response, 'title6')
        self.assertContains(response, 'comment6')


class ArticleUpdatePageTests(TestCase):

    def setUp(self) -> None:
        self.user = CustomUser.objects.create(
            username='username7',
            email='username7@gmail.com',
            password='123456',
            age=35
        )
        self.article = Article.objects.create(
            title='title7',
            content='content7',
            date=datetime.datetime.now(),
            author=self.user
        )
        self.comment = Comment.objects.create(
            comment='comment7',
            author=self.user,
            article=self.article
        )

    def test_article_update_page_status_code_unauthenticated(self):
        response = self.client.post(reverse('article_new'), {
            'title': 'title8',
            'content': 'content8',
        })
        self.assertEqual(response.status_code, 302)

        self.assertTrue(reverse('login') in response.url)

    def test_article_update_page_status_code_authenticated(self):
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('article_new'), {
            'title': 'title8',
            'content': 'content8',
        })
        self.assertEqual(response.status_code, 302)

        url_pattern = re.compile(r'/articles/\d+/')
        self.assertTrue(re.match(url_pattern, response.url) is not None)


class ArticleDeletePageTests(TestCase):

    def setUp(self) -> None:
        self.user = CustomUser.objects.create(
            username='username8',
            email='username8@gmail.com',
            password='123456',
            age=34
        )
        self.article = Article.objects.create(
            title='title8',
            content='content8',
            date=datetime.datetime.now(),
            author=self.user
        )
        self.comment = Comment.objects.create(
            comment='comment8',
            author=self.user,
            article=self.article
        )

    def test_article_delete_page_status_code_unauthenticated(self):
        response = self.client.get(reverse('article_delete', args=[str(self.article.pk)]))
        self.assertEqual(response.status_code, 302)

        self.assertTrue(reverse('login') in response.url)

    def test_article_delete_page_status_code_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('article_delete', args=[str(self.article.pk)]))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'articles/article_delete.html')


class ArticleDetailPageTests(TestCase):

    def setUp(self) -> None:
        self.user = CustomUser.objects.create(
            username='username9',
            email='username9@gmail.com',
            password='123456',
            age=34
        )
        self.article = Article.objects.create(
            title='title9',
            content='content9',
            date=datetime.datetime.now(),
            author=self.user
        )
        self.comment = Comment.objects.create(
            comment='comment9',
            author=self.user,
            article=self.article
        )

    def test_article_detail_page_status_code_unauthenticated(self):
        response = self.client.get(reverse('article_detail', args=[str(self.article.pk)]))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(reverse('login') in response.url)

    def test_article_detail_page_status_code_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('article_detail', args=[str(self.article.pk)]))

        self.assertEqual(response.status_code, 200)

    def test_template_used_by_detail_page_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('article_detail', args=[str(self.article.pk)]))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'articles/article_detail.html')

        self.assertContains(response, 'username9')
        self.assertContains(response, 'username9')
        self.assertContains(response, 'comment9')
