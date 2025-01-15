from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import FormularioDePostagem, FormularioDeLogin
from .models import CustomUser, Posts
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def home_page(request):
    return render(request, 'blog/home_page.html', {})

def pagina_de_acesso(request):
    if request.method == "POST":
        formulario_de_login = FormularioDeLogin(request.POST)
        if formulario_de_login.is_valid():
            email = formulario_de_login.cleaned_data['email']
            senha = formulario_de_login.cleaned_data['senha']
            usuario = authenticate(request, username=email, password=senha)
            if usuario is not None:
                login(request, usuario)
                return redirect('posts')
            else:
                messages.error(request, 'Email ou senha inválidos')
    formulario_de_login = FormularioDeLogin()
    return render(request, 'blog/pagina_de_acesso.html', {'form_login': formulario_de_login})

@login_required
def deslogar(request):
    logout(request)
    return redirect('home_page')
        
@login_required
def posts(request):
    if request.method == "POST":
        formulario_de_postagem = FormularioDePostagem(request.POST, request.FILES)
        if formulario_de_postagem.is_valid():
            nova_postagem = formulario_de_postagem.cleaned_data
            post = Posts(
                autor = request.user,
                titulo = nova_postagem['titulo'],
                descricao = nova_postagem['descricao'],
                imagem = nova_postagem['imagem']
            ) 
            post.save()
            return redirect('posts')
    else:
        formulario_de_postagem = FormularioDePostagem()
    posts = Posts.objects.filter(data_publicacao__lte=timezone.now()).order_by('-data_publicacao')
    return render(request, 'blog/posts.html', {'posts': posts,'form': formulario_de_postagem})

@login_required
def detalhes(request, id):
    post = Posts.objects.get(id=id)
    return render(request, 'blog/detalhes.html', {'post': post})

@login_required
def apagar_postagem(request, id):
    post = Posts.objects.get(id=id)
    if request.method == "POST":
        post.delete()
    return redirect('posts')



