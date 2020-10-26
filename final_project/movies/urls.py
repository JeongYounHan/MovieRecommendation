from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('adm_search/',views.adm_search, name='adm_search'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('<int:movie_pk>/<str:username>/rating/', views.rating_create, name='rating_create'),
    path('<int:movie_pk>/rating/<int:rating_pk>/delete/', views.rating_delete, name='rating_delete'),
    path('manage/', views.manage, name='manage'),
    path('movie_create/', views.movie_create, name='movie_create'),
    path('<int:movie_pk>/movie_detail', views.movie_detail, name='movie_detail'),
    path('<int:movie_pk>/update', views.movie_update, name='movie_update'),
    path('<int:movie_pk>/movie_delete', views.movie_delete, name='movie_delete'),
    # path('<int:user_pk>/recommend/', views.recommend, name='recommend'),
    ]