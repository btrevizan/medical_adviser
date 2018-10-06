from django import forms
from pycpfcnpj import cpfcnpj as cpf
from pycpfcnpj.compatible import clear_punctuation
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    NONE = 0
    DOCTOR = 1
    PATIENT = 2

    first_name = forms.CharField(max_length=30,
                                 widget=forms.TextInput(attrs={'placeholder': 'Nome', 'class': 'form-control'}))

    last_name = forms.CharField(max_length=30,
                                widget=forms.TextInput(attrs={'placeholder': 'Sobrenome', 'class': 'form-control'}))

    email = forms.EmailField(max_length=254,
                             widget=forms.EmailInput(attrs={'placeholder': 'E-mail', 'class': 'form-control'}))

    type = forms.ChoiceField(choices=((NONE, 'Tipo da conta'), (DOCTOR, 'Médico'), (PATIENT, 'Paciente')),
                             widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'placeholder': 'Nome do usuário (utlizado no login)',
                                                     'class': 'form-control'})

        self.fields['password1'].widget.attrs.update({'placeholder': 'Senha',
                                                      'class': 'form-control'})

        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirmação da Senha',
                                                      'class': 'form-control'})

        self.error_messages['invalid_type'] = "Você precisa selecionar um tipo de conta."

    def clean_type(self):
        typed_type = int(self.cleaned_data['type'])
        if typed_type == self.NONE:
            raise forms.ValidationError(
                self.error_messages['invalid_type'],
                code='invalid_type',
            )

        return int(self.cleaned_data['type'])


class SignUpPatientForm(forms.Form):
    cpf = forms.CharField(max_length=11,
                          widget=forms.TextInput(attrs={'placeholder': 'CPF (apenas dígitos)', 'class': 'form-control'}))

    city = forms.CharField(max_length=70,
                           widget=forms.TextInput(attrs={'placeholder': 'Cidade', 'class': 'form-control'}))

    uf = forms.CharField(max_length=2,
                         widget=forms.TextInput(attrs={'placeholder': 'UF', 'class': 'form-control'}))

    error_messages = {
        'invalid_cpf': 'CPF inválido.'
    }

    def clean_cpf(self):
        typed_cpf = clear_punctuation(self.cleaned_data['cpf'])
        if not cpf.validate(typed_cpf):
            raise forms.ValidationError(
                self.error_messages['invalid_cpf'],
                code='invalid_cpf'
            )

        return typed_cpf

    def clean_uf(self):
        return self.cleaned_data['uf'].upper()


class SignUpDoctorForm(forms.Form):
    crm = forms.CharField(max_length=6,
                          widget=forms.TextInput(attrs={'placeholder': 'CRM (apenas dígitos)', 'class': 'form-control'}))

    crm_uf = forms.CharField(max_length=2,
                             widget=forms.TextInput(attrs={'placeholder': 'UF do CRM', 'class': 'form-control'}))

    speciality = forms.CharField(max_length=25,
                                 widget=forms.TextInput(attrs={'placeholder': 'Especialidade', 'class': 'form-control'}))

    def clean_crm_uf(self):
        return self.cleaned_data['crm_uf'].upper()


class SignUpAddressForm(forms.Form):
    uf = forms.CharField(max_length=2,
                         widget=forms.TextInput(attrs={'placeholder': 'UF', 'class': 'form-control'}))

    city = forms.CharField(max_length=40,
                           widget=forms.TextInput(attrs={'placeholder': 'Cidade', 'class': 'form-control'}))

    neighborhood = forms.CharField(max_length=40,
                                   widget=forms.TextInput(attrs={'placeholder': 'Bairro', 'class': 'form-control'}))

    street = forms.CharField(max_length=100,
                             widget=forms.TextInput(attrs={'placeholder': 'Rua', 'class': 'form-control'}))

    number = forms.CharField(max_length=6,
                             widget=forms.TextInput(attrs={'placeholder': 'Número', 'class': 'form-control'}))

    complement = forms.CharField(max_length=15, required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Complemento', 'class': 'form-control'}))

    def clean_uf(self):
        return self.cleaned_data['uf'].upper()
