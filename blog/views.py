from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from .forms import FormularioDeCadastro
from .models import CustomUser, Posts
from django.utils import timezone

# Create your views here.

def home_page(request):
    return render(request, 'blog/home_page.html', {})

def pagina_de_acesso(request):
    if request.method == "POST":
        if 'login' in request.POST:
            username = request.POST['input_email']
            password = request.POST['input_senha']
            # return HttpResponse(f"<p>{email} e {password}</p>")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('posts')
        elif 'cadastro' in request.POST:
            nome = request.POST['nome_usuario']
            sobrenome = request.POST['sobrenome_usuario']
            apelido = request.POST['apelido_usuario']
            email = request.POST['email_usuario']
            senha = request.POST['senha_usuario']
            #mensagem = f"Usuário {nome} {sobrenome}, email : {email} e senha: {senha}"
            user = CustomUser.objects.create_user(username=apelido, email=email, password=senha, first_name=nome, last_name=sobrenome)
            user.save()
            user = authenticate(request, username=apelido, password=senha)
            login(request, user)
            return redirect('posts')
    return render(request, 'blog/pagina_de_acesso.html', {})
    
def deslogar(request):
    logout(request)
    return redirect('home_page')
        
    
def posts(request):
    posts = Posts.objects.filter(data_publicacao__lte=timezone.now()).order_by('-data_publicacao')
    return render(request, 'blog/posts.html', {'posts': posts})




