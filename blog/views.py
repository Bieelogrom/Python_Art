from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from .forms import FormularioDePostagem, FormularioDeLogin, FormularioDeRegistro
from .models import CustomUser, Posts, PostagensSalvas
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
import re

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
                    return redirect('posts', 1)
                else:
                    messages.error(request, 'Email ou senha inválidos')
        elif 'botao_registar' in request.POST:
            """
                Necessário inserir uma senha de até 8 chars para criar a conta.
            """
            formulario_de_registro = FormularioDeRegistro(request.POST)
            if formulario_de_registro.is_valid():
                usuario = formulario_de_registro.cleaned_data
                novo_usuario = CustomUser(
                    first_name = usuario['first_name'],
                    last_name = usuario['last_name'],
                    username = usuario['username'],
                    email = usuario['email'],
                )
                novo_usuario.set_password(usuario['password'])
                novo_usuario.save()
                return redirect('pagina_de_acesso')
    formulario_de_registro = FormularioDeRegistro()
    formulario_de_login = FormularioDeLogin()
    return render(request, 'blog/pagina_de_acesso.html', {'form_login': formulario_de_login, 'form_registro': formulario_de_registro})

def validacao_de_senha(request):
    if request.method == "POST":
        senha = request.POST.get('password', '')
        
        erros = []
        
        if len(senha) < 8:
            erros.append("Senha precisa ter 8 ou mais carácteres!")
        if not re.search(r'[A-Z]', senha):
            erros.append("A senha deve conter pelo menos uma letra maiúscula!")
        if not re.search(r'[a-z]', senha):
            erros.append("A senha deve conter pelo menos uma letra minúscula!")
        if not re.search(r'[0-9]', senha):
            erros.append("A senha deve conter pelo menos um número!")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
            erros.append("A senha deve conter pelo menos um caractere especial!")
        
        if erros:
            return JsonResponse({'valido': False, 'erros': erros})
        else: 
            return JsonResponse({'valido': True})
    return JsonResponse({'error': 'Método não permitido!'}, status=405)

@login_required
def deslogar(request):
    logout(request)
    return redirect('home_page')
        
@login_required
def posts(request, categoria):
    if categoria == 1:
        posts = Posts.objects.annotate(num_salvos=Count('postagenssalvas')).order_by('-num_salvos', '-data_publicacao')
    elif categoria == 2:
        posts = Posts.objects.filter(data_publicacao__lte=timezone.now()).order_by('-data_publicacao')
    else:
        posts = Posts.objects.filter(data_publicacao__lte=timezone.now()).order_by('-data_publicacao')
    return render(request, 'blog/posts.html', {'posts': posts})

@login_required
def detalhes(request, id):
    post = Posts.objects.get(id=id)
    salvo = PostagensSalvas.objects.filter(id_postagem_salva=post, id_usuario_que_salvou=request.user)
    return render(request, 'blog/detalhes.html', {'post': post, 'salvo': salvo})

@login_required
def fazer_postagem(request):
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
            return redirect('posts', 1)
    else:
        formulario_de_postagem = FormularioDePostagem()
    return render(request, 'blog/postagem.html', {'form': formulario_de_postagem})

@login_required
def apagar_postagem(request, id):
    post = get_object_or_404(Posts, id=id)
    if request.method == "POST":
        post.delete()
    return redirect('posts', 1)

@login_required
def salvar_postagem(request, id):
    usuario = CustomUser.objects.get(id=request.user.id)
    postagem = Posts.objects.get(id=id)
    postagens_salvas = PostagensSalvas.objects.filter(id_usuario_que_salvou=usuario, id_postagem_salva=postagem).first()
    if postagens_salvas:
        postagens_salvas.delete()
        return redirect("perfil")
    else:
        nova_postagem_salva = PostagensSalvas(id_usuario_que_salvou=usuario, id_postagem_salva=postagem)
        nova_postagem_salva.save()
        # mensagem = f"<p>ID da publicação : {id}</br>ID do usuário: {request.user.id}</p>"
    return redirect("perfil")

@login_required
def editar_postagem(request, id):
    postagem = get_object_or_404(Posts, id=id)
    if request.method == "POST":
        form = FormularioDePostagem(request.POST, request.FILES, instance=postagem)
        if form.is_valid():
            form.save()
        return redirect("posts", 2)
    else:
        form = FormularioDePostagem(instance=postagem)
    return render(request, 'blog/postagem.html', {'form': form})

@login_required
def perfil(request):
    contagem_de_salvos = PostagensSalvas.objects.filter(id_usuario_que_salvou=request.user.id).count()
    postagens_salvas_pelo_usuario = PostagensSalvas.objects.filter(id_usuario_que_salvou=request.user).select_related('id_postagem_salva')
    # return HttpResponse(contagem_de_salvos)
    return render(request, 'blog/perfil.html', {'contagem_de_salvos': contagem_de_salvos, 'postagens_salvas_pelo_usuario': postagens_salvas_pelo_usuario})

@login_required
def opcoes(request):
    return render(request, 'blog/opcoes.html', {})

