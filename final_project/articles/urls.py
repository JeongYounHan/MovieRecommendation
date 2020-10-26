from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('<int:article_pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:article_pk>/comments/', views.comments_create, name='comments_create'),
    path('<int:article_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
    path('<int:article_pk>/comments/<int:comment_pk>/update/', views.comments_update, name='comments_update'),
    path('<int:article_pk>/like/', views.like, name='like'),
    path('<int:article_pk>/delete/', views.article_delete, name='article_delete'),
    path('<int:article_pk>/article_update', views.article_update, name='article_update'),

]