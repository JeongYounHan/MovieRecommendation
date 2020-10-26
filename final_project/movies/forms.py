from django import forms
from .models import Rating, Movie

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['ratings', 'content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'한줄평을 남겨주세요.'}),
        }


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'poster_path', 'vote_average', 'overview', 'genres']