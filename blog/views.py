from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def home_page(request):
    return render(request, 'blog/home_page.html', {})

def pagina_de_acesso(request):
    if request.method == "POST":
        username = request.POST['input_email']
        password = request.POST['input_senha']
        # return HttpResponse(f"<p>{email} e {password}</p>")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('posts', {'user': user})
    return render(request, 'blog/pagina_de_acesso.html', {})
    
def posts(request):
    return render(request, 'blog/posts.html', {})




