from django import forms
from dash.models import Rating


class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = ('description', 'stars')