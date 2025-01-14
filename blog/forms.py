from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Posts

class FormularioDeCadastro(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']
        
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

    
        