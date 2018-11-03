from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegisterAdminForm(UserCreationForm):

    first_name = forms.CharField(max_length=30,
                                 widget=forms.TextInput(attrs={'placeholder': 'Nome', 'class': 'form-control'}))

    last_name = forms.CharField(max_length=30,
                                widget=forms.TextInput(attrs={'placeholder': 'Sobrenome', 'class': 'form-control'}))

    email = forms.EmailField(max_length=254,
                             widget=forms.EmailInput(attrs={'placeholder': 'E-mail', 'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'placeholder': 'Nome do usuário (utlizado no login)',
                                                     'class': 'form-control'})

        self.fields['password1'].widget.attrs.update({'placeholder': 'Senha',
                                                      'class': 'form-control'})

        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirmação da Senha',
                                                      'class': 'form-control'})