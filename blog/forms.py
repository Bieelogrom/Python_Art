from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Posts, CustomUser


class FormularioDeLogin(forms.Form):
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search'}))
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Search'}))
        
class FormularioDePostagem(forms.ModelForm):
    class Meta:
        model = Posts
        
        fields = ['titulo', 'descricao', 'imagem']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={"rows":"4", "cols":"50", 'class': 'form-control'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'titulo': 'Título da postagem',
            'descricao': 'Descrição da postagem',
            'imagem': 'Imagem da postagem',
        }
        
class FormularioDeRegistro(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme sua senha...'}), label="Confirmar senha")
    class Meta:
        model = get_user_model()
        fields = [
            'first_name', 'last_name', 'username', 'email', 'password'
        ]
        exclude = (
            'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu primeiro nome...'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu sobrenome...'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Um apelido...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Um email válido...'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Uma senha segura...'}),
        }
        labels = {
            'first_name': 'Primeiro nome',
            'last_name': 'Sobrenome',
            'username': 'Apelido',
            'email': 'E-mail',
            'password': 'Senha'
        }
        

    
        