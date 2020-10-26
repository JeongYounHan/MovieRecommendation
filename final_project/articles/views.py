from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages


## 게시판 보기
def index(request):
    articles = Article.objects.all()


    context = {
        'articles': articles,
    }

    return render(request, 'articles/index.html', context)


## 게시글 작성
@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/form.html', context)



## 게시글 상세 보기
def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    # 댓글 목록
    comments = article.comment_set.order_by('-pk')

    # 댓글 작성 form
    comment_form = CommentForm()

    context = {
        'article': article,
        'comments' : comments,
        'comment_form': comment_form,
    }
    return render(request, 'articles/detail.html', context)

@require_POST
def comments_create(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)

        # 댓글 저장
        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                # 1:N 관계를 지정: commit=False를 통해
                comment = comment_form.save(commit=False)
                comment.article = article
                comment.user = request.user
                comment.save()

        return redirect('articles:detail', article_pk)

## 댓글 삭제
@require_POST
def comments_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if comment.user == request.user or request.user.username == 'admin':
        comment.delete()
        return redirect('articles:detail', article_pk)



# 게시글 좋아요 누르기
@login_required
def like(request, article_pk):
    user = request.user
    article = get_object_or_404(Article, pk=article_pk)

    if article.article_like_users.filter(pk=user.pk).exists():
        article.article_like_users.remove(user)
        # 좋아요 취소
        liked = False
    else:
        article.article_like_users.add(user)
        # 좋아요 등록
        liked = True

    context = {
        'liked': liked,
        # 좋아요 개수
        'count': article.article_like_users.count()
    }
    return JsonResponse(context)


## 댓글 수정

## 댓글 수정
@login_required
def comments_update(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        commentform = CommentForm(request.POST, instance=comment)
        if commentform.is_valid():
            comment = commentform.save(commit=False)
            if request.user.username == 'admin':
                comment.user = comment.user
            else:
                comment.user = request.user
            comment.save()
            return redirect('articles:detail', article.pk)
        else:
            commentform = CommentForm(instance=comment)
        context = {
            'commentform':commentform
        }
        return render(request, 'articles/comment_form.html', context)
    return redirect('articles:detail', article.pk)



#게시글 삭제
@require_POST
def article_delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if article.user == request.user  or request.user.username == 'admin':
        article.delete()
        articles = Article.objects.all()
        context = {
            'articles': articles,
        }
        return render(request, 'articles/index.html', context)


#게시글 수정
@require_POST
def article_update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if article.user == request.user or request.user.username == 'admin':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
        context = {
            'form':form
        }
        return render(request, 'articles/form.html', context)
    else:
        return redirect('aritlces:detail', article.pk )




# 게시글 검색
def search(request):
    qs = Article.objects.all()

    q = request.GET.get('q', '') # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    if q: # q가 있으면
        qs = qs.filter(movie__title__icontains=q) # 제목에 q가 포함되어 있는 레코드만 필터링

    return render(request, 'articles/index.html', {
        'articles' : qs,
        'q' : q,
    })




