from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from .models import Movie, Genre, Rating
from .forms import RatingForm, MovieForm
from django.db.models import Count, Avg
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.contrib import messages
import os

# Create your views here.
User = get_user_model()

def main(request):
    API_KEY = os.environ.get('API_KEY')
    context = {
        'API_KEY': API_KEY,
    }
    return render(request, 'movies/main.html', context)


def index(request):
    movies = Movie.objects
    movie_list = Movie.objects.all()
    paginator = Paginator(movie_list, 12)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'movies': movies,
        'page':page,
        'posts': posts,
    }
    return render(request, 'movies/index.html', context)


# 영화 디테일(평점) 창( movie 평점 계산해서 넘겨주기)
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    API_KEY2 = os.environ.get('API_KEY2')
    # 평점 목록
    ratings = movie.rating_set.order_by('-pk')
    rating_form = RatingForm()

    # 평균점수 계산
    average = Rating.objects.filter(movie=movie).aggregate(Avg('ratings'))

    context = {
        'movie': movie,
        'ratings' : ratings,
        'form': rating_form,
        'average': average,
        'API_KEY2': API_KEY2,
    }
    return render(request, 'movies/detail.html', context)


@login_required
def rating_create(request, movie_pk, username):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user_temp = get_object_or_404(User, username=username)
    ratings = Rating.objects.filter(movie=movie_pk)
    average = Rating.objects.filter(movie=movie).aggregate(Avg('ratings'))

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            for rating in ratings:
                if user_temp == rating.user:
                    context = {
                        'movie': movie,
                        'ratings' : ratings,
                        'form': form,
                        'average': average,
                    }
                    messages.warning(request, '이미 평점을 남기셨습니다.')
                    return render(request, 'movies/detail.html',context)

            else:
                rating = form.save(commit=False)
                rating.user = request.user
                rating.movie = movie
                rating.save()
                return redirect('movies:detail', movie.pk)

    # 10점 이상의 값 입력하면 에러뜨게 페이지 렌더링 해야
    context = {
        'movie': movie,
        'ratings' : ratings,
        'form': form,
        'average': average,
    }
    return render(request, 'movies/detail.html', context)


@require_POST
def rating_delete(request, movie_pk, rating_pk):
    rating = Rating.objects.get(pk=rating_pk)
    rating.delete()
    return redirect('movies:detail', movie_pk)



@login_required
def like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)

    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        # 좋아요 취소
        liked = False
    else:
        movie.like_users.add(user)
        # 좋아요 등록
        liked = True

    context = {
        'liked': liked,
        # 좋아요 개수
        'count': movie.like_users.count()
    }
    return JsonResponse(context)


# 영화 검색
def search(request):
    qs = Movie.objects.all()

    q = request.GET.get('q', '') # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    if q: # q가 있으면
        qs = qs.filter(title__icontains=q) # 제목에 q가 포함되어 있는 레코드만 필터링

    # 페이지네이터 사용하면 한글자밖에 검색 안됨
    # paginator = Paginator(qs, 12)
    # page = request.GET.get('page')
    # posts = paginator.get_page(page)

    return render(request, 'movies/index.html', {
        'posts' : qs,
        'q' : q,
    })


## 관리자에서 검색
def adm_search(request):
    qs = Movie.objects.all()
    print(request)
    q = request.GET.get('q', '') # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    if q: # q가 있으면
        qs = qs.filter(title__icontains=q) # 제목에 q가 포함되어 있는 레코드만 필터링

    # 페이지네이터 사용하면 한글자밖에 검색 안됨
    # paginator = Paginator(qs, 12)
    # page = request.GET.get('page')
    # posts = paginator.get_page(page)

    return render(request, 'movies/manage.html', {
        'posts' : qs,
        'q' : q,
    })


#관리자 페이지

def manage(request):
    movies = Movie.objects.all()
    movie_list = Movie.objects.all()
    paginator = Paginator(movie_list, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'movies': movies,
        'page':page,
        'posts': posts,
    }
    return render(request, 'movies/manage.html', context)



# 관리자 - 영화등록
@login_required
def movie_create(request):
    if request.method=='POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save()

            return redirect('movies:movie_detail', movie.pk)
    else:
        form = MovieForm()
        context = {
        'form':form
    }
    return render(request, 'movies/form.html', context)



# 관리자 - 영화수정
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.user.username=='admin':
        context = {
            'movie':movie,
        }
        return redirect('movies:movie_detail', movie.pk)



## 영화업데이트
@require_POST
def movie_update(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.user.username == 'admin':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.save()
            return redirect('movies:movie_detail', movie.pk)
        else:
            form = MovieForm(instance=movie)
        context = {
            'form':form
        }
        return render(request, 'movies/form.html', context)
    else:
        return redirect('movies:movie_detail', movie.pk)



## 영화삭제
@require_POST
def movie_delete(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.user.username=='admin':
        movie.delete()
        return redirect('movies:manage')