from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import Movie, Genre
from django.db.models import Count
from django.core.paginator import Paginator


# Create your views here.

def index(request):
    movies = Movie.objects
    movie_list = Movie.objects.all()
    paginator = Paginator(movie_list, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'movies': movies,
        'page':page,
        'posts': posts,
    }
    return render(request, 'movies/index.html', context)


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

    # html을 그대로 보내주는 >>> jsonresponse
    # return redirect('articles:index')

    context = {
        'liked': liked,
        # 좋아요 개수
        'count': movie.like_users.count()
    }
    return JsonResponse(context)

def recommend(request, user_pk):
    User = get_user_model()
    person = get_object_or_404(User, pk=user_pk)
    person_movies = Movie.objects.filter(like_users=person)
    person_genres = person_movies.values('genres').annotate(total=Count('genres')).order_by('-total')[:1]
    gen = Genre.objects.all()


    context = {
        'person': person,
        'person_genres': person_genres,
        'gen':gen,
    }
    return render(request, 'movies/recommend.html', context)

