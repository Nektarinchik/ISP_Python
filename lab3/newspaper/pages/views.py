import logging

from django.shortcuts import render
from django.views.generic import ListView

import users.models

from articles.views import logger


class HomepageView(ListView):
    logger.info('enter to HomePageView')
    template_name = 'home.html'
    model = users.models.CustomUser
