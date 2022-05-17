from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk_c>/edit/', views.CommentEditView.as_view(), name='comment_edit'),
    path('<int:pk_c>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('new/', views.CommentCreateView.as_view(), name='comment_new')
]
