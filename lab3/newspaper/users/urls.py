from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('<int:pk>/articles/', views.AuthorArticlesListView.as_view(), name='users/author_articles')
]
