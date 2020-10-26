from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from django.db.models import Count, Avg
import requests
from bs4 import BeautifulSoup
from movies.models import Genre, Movie, Rating

User = get_user_model()
# 회원가입
def signup(request):
    # POST로 들어올때
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            # 로그인시 그전 경로로 돌아가게 수정
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


# 로그인기능
def login(request):
    if request.method == 'POST':
        # AuthenticationForm에서 request를 받아서쓴다..
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # 로그인시 그전 경로로 돌아가게 수정
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


# 로그아웃 - 로그인 상태에서만 가능
@login_required
def logout(request):
    auth_logout(request)
    return redirect('/')


# 마이페이지(영화추천 여기서?) 수정


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)

    res_list = []

    API_KEY = 'AIzaSyBV5lXg9aqyiX7QNhoYPc5dUkVeyPnEnSI'
    for movie in user.like_movies.all():
        a = movie.title
        API_URL = "https://www.googleapis.com/youtube/v3/search?key=AIzaSyDlX-4f4HUFZn014hBI7FXTNHCo7pgnQQg&part=id&q="+a+" 예고편"
        print(API_URL)
        res = requests.get(API_URL)
        res = res.json()
        print(res)

        # 오류 땜에 오후 4시 리셋? 이거 detail 창에 하는게 더 좋을듯
        # 보고싶어요 목록에서 누르면 디테일 창으로 가고
        # for i in res['items']:
        #     res_list.append(i['id'])
        #     break

    context = {
        'user': user,
        'res_list':res_list,

    }

    return render(request, 'accounts/profile.html', context)


# 팔로우 기능
@login_required
def follow(request, username):
    person = get_object_or_404(User, username=username)
    user = request.user
    if person != user:
        if person.followers.filter(pk=user.pk).exists():
            person.followers.remove(user)
        else:
            person.followers.add(user)

    return redirect('accounts:profile', username)


# 추천 기능
def recommend(request, username):
    person = get_object_or_404(User, username=username)

    # 해당 유저가 평점 높게 준 영화 상위 20개 추출
    person_ratings = Rating.objects.filter(user=person).order_by('-ratings')[:20]

    # 10개의 영화에서 등장하는 장르들 딕셔너리로 정리
    genre_dict = {}

    for temp in person_ratings:
        for genre in temp.movie.genres.all():
            if genre in genre_dict:
                genre_dict[genre] += 1
            else:
                genre_dict[genre] = 1

    # 딕셔너리 value 값(장르 등장 횟수) 기준 내림차순 정렬
    genres_dict = sorted(genre_dict.items(), key=lambda x: x[1], reverse=True)

    # 상위 랭크된 장르 3개 뽑기(3개 안채워질수도 있음)
    genres_rank = []
    for key, val in genres_dict:
        if len(genres_rank) >= 3:
            break
        else:
            genres_rank.append(key)


    # 추천 영화 넣기
    recommendations = []
    # 장르 3개 다 채워져 있을 때(3개 다 포함하는 영화 별로 없을수도 있으므로 분기)
    if len(genres_rank) == 3:
        for movie in Movie.objects.all():
            # 1순위: 3개 장르 다 들어있는 영화
            if genres_rank[0] in movie.genres.all() and genres_rank[1] in movie.genres.all() and genres_rank[2] in movie.genres.all():
                # 이미 평가 내린 영화 목록에 해당 영화 들어있으면 추천x
                if movie not in Movie.objects.filter(rating__user=person):
                    recommendations.append(movie)
                if len(recommendations) >= 8:
                    break
        else: # 8개 추천영화 목록 다 차지 않았을 때
            for movie in Movie.objects.all():
                # 2순위: 앞의 2개 장르 들어있는 영화
                if genres_rank[0] in movie.genres.all() and genres_rank[1] in movie.genres.all():
                    if movie not in Movie.objects.filter(rating__user=person):
                        recommendations.append(movie)
                    if len(recommendations) >= 8:
                        break
            else: # 8개 추천영화 목록 다 차지 않았을 때
                for movie in Movie.objects.all():
                    # 3순위: 앞의 1개 장르 들어있는 영화
                    if genres_rank[0] in movie.genres.all():
                        if movie not in Movie.objects.filter(rating__user=person):
                            recommendations.append(movie)
                        if len(recommendations) >= 8:
                            break
    # 장르 2개 뿐일 때
    elif len(genres_rank) == 2:
        for movie in Movie.objects.all():
            if genres_rank[0] in movie.genres.all() and genres_rank[1] in movie.genres.all():
                if movie not in Movie.objects.filter(rating__user=person):
                    recommendations.append(movie)
                if len(recommendations) >= 8:
                    break
        else: # 8개 추천영화 목록 다 차지 않았을 때
            for movie in Movie.objects.all():
                # 앞의 1개 장르 들어있는 영화
                if genres_rank[0] in movie.genres.all():
                    if movie not in Movie.objects.filter(rating__user=person):
                        recommendations.append(movie)
                    if len(recommendations) >= 8:
                        break
    else:
        for movie in Movie.objects.all():
            # 앞의 1개 장르 들어있는 영화
            if genres_rank[0] in movie.genres.all():
                if movie not in Movie.objects.filter(rating__user=person):
                    recommendations.append(movie)
                if len(recommendations) >= 8:
                    break


    context = {
        'person': person,
        'person_ratings': person_ratings,
        'recommendations': recommendations,
        'genres_rank': genres_rank,
    }
    return render(request, 'accounts/recommend.html', context)


