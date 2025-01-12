from django.shortcuts import render


# Create your views here.

def home_page(request):
    return render(request, 'blog/home_page.html', {})

def pagina_de_acesso(request):
    return render(request, 'blog/pagina_de_acesso.html', {})


