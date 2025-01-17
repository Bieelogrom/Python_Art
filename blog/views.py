from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import FormularioDePostagem, FormularioDeLogin, FormularioDeRegistro
from .models import CustomUser, Posts, PostagensSalvas
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def home_page(request):
    return render(request, 'blog/home_page.html', {})

def pagina_de_acesso(request):
    if request.method == "POST":
        if 'botao_login' in request.POST:
            formulario_de_login = FormularioDeLogin(request.POST)
            if formulario_de_login.is_valid():
                email = formulario_de_login.cleaned_data['email']
                senha = formulario_de_login.cleaned_data['senha']
                # return HttpResponse(f'Email: {email} Senha: {senha}')
                usuario = authenticate(request, username=email, password=senha)
                # return HttpResponse(usuario)
                if usuario is not None:
                    login(request, usuario)
                    return redirect('posts')
                else:
                    messages.error(request, 'Email ou senha inválidos')
        elif 'botao_registar' in request.POST:
            """
                Necessário inserir uma senha de até 8 chars para criar a conta.
            """
            formulario_de_registro = FormularioDeRegistro(request.POST)
            if formulario_de_registro.is_valid():
                usuario = formulario_de_registro.cleaned_data
                if usuario['password1'] == usuario['password2']:
                    novo_usuario = CustomUser(
                        first_name = usuario['first_name'],
                        last_name = usuario['last_name'],
                        username = usuario['username'],
                        email = usuario['email'],
                    )
                    novo_usuario.set_password(usuario['password1'])
                    novo_usuario.save()
                    return redirect('pagina_de_acesso')
    formulario_de_registro = FormularioDeRegistro()
    formulario_de_login = FormularioDeLogin()
    return render(request, 'blog/pagina_de_acesso.html', {'form_login': formulario_de_login, 'form_registro': formulario_de_registro})

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
    post = get_object_or_404(Posts, id=id)
    if request.method == "POST":
        post.delete()
    return redirect('posts')

@login_required
def salvar_postagem(request, id):
    usuario = CustomUser.objects.get(id=request.user.id)
    postagem = Posts.objects.get(id=id)
    if usuario in PostagensSalvas.objects.all():
        print("oi")
    else:
        nova_postagem_salva = PostagensSalvas(id_usuario_que_salvou=usuario, id_postagem_salva=postagem)
        nova_postagem_salva.save()
    # mensagem = f"<p>ID da publicação : {id}</br>ID do usuário: {request.user.id}</p>"
    # return HttpResponse(mensagem)
    return redirect("posts")

@login_required
def perfil(request):
    contagem_de_salvos = CustomUser.objects.filter(id=request.user.id).count()
    return render(request, 'blog/perfil.html', {'contagem_de_salvos': contagem_de_salvos})



