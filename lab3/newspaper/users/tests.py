import datetime
import logging

from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from articles.models import Article
from .models import CustomUser
from .views import AuthorArticlesListView

logger = logging.getLogger('main')


class AuthorArticlesPageTests(TestCase):

    def setUp(self) -> None:
        self.user = CustomUser.objects.create(
            username='username1',
            email='username1@gmail.com',
            password='123456',
            age=18
        )
        self.article = Article.objects.create(
            title='title1',
            content='content1',
            date=datetime.datetime.now(),
            author=self.user
        )

    def test_author_articles_page_status_code_unauthenticated(self):
        response = self.client.get(reverse('users/author_articles', args=[str(self.user.pk)]))

        self.assertEqual(response.status_code, 302)

    def test_author_articles_page_status_code_authenticated(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('users/author_articles', args=[str(self.user.pk)]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'username1')

    def test_author_articles_page_template_used(self):
        self.client.force_login(user=self.user)
        logger.debug(self.user.pk)
        response = self.client.get(reverse('users/author_articles', args=[str(self.user.pk)]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/author_articles.html')


class LogInPageTests(TestCase):

    def setUp(self) -> None:
        self.credentials = {
            'username': 'login_test_user',
            'password': '123456'
        }
        CustomUser.objects.create_user(**self.credentials)

    def test_signup_page_status_code(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_template_used_by_signup_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_form(self):
        response = self.client.post(reverse('login'), self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)

