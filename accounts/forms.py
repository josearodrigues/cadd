import re
from django import forms
from django.contrib.auth.models import User

from django.forms import TextInput, PasswordInput, HiddenInput

class UsuarioForm(forms.ModelForm):
    """
    Classe de uso do sistema para o formulário de registro
    """

    new_password1 = forms.CharField(widget=forms.PasswordInput(
                    attrs={'class': 'form-control', 'data-rules': 'required',
                           'placeholder': 'Informe a nova senha'}))

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        widgets = {
            'username': TextInput(attrs={'class': 'form-control',
                                          'data-rules': 'required',
                                          'placeholder': 'Informe a matrícula'}),
            'password': PasswordInput(attrs={'class': 'form-control',
                                         'data-rules': 'required',
                                         'placeholder': 'Informe a senha'}),
        }

    def clean(self):
        if User.objects.filter(username=self.cleaned_data.get('username')):
            raise forms.ValidationError("Matrícula já registrada!")
        if (self.cleaned_data.get('password') !=
                self.cleaned_data.get('new_password1')):
            raise forms.ValidationError("Senhas diferentes!")
        if len(self.cleaned_data.get('password')) < 8:
            raise forms.ValidationError(
                    "Senha tem que ter no mínimo 8 caracteres!"
                )
        if len(re.findall(r"[A-Z]", self.cleaned_data.get('password'))) < 1:
            raise forms.ValidationError(
                    "Senha tem que ter no mínimo 1 letra maiúscula!"
                )
        if len(re.findall(r"[0-9]", self.cleaned_data.get('password'))) < 1:
            raise forms.ValidationError("Senha tem que ter no mínimo 1 número!")
#        if len(re.findall(r"[~`!@#$%^&*()_+=-{};:'><]", self.cleaned_data.get('password'))) < 1:
#            raise forms.ValidationError("Senha tem que ter no mínimo 1 caracter especial")

        return self.cleaned_data
