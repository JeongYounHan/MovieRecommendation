from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['movie', 'title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'제목을 입력해주세요.'},),
        },


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'댓글을 남겨보세요.'},),
        }
