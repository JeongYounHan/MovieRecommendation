from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # 마이페이지
    path('<str:username>/', views.profile, name='profile'),
    # 퐐로우
    path('<str:username>/follow/', views.follow, name='follow'),
    # 영화추천
    path('<str:username>/recommend/', views.recommend, name='recommend'),
    ]