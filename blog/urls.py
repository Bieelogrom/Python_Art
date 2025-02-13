from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('pagina_de_acesso/', views.pagina_de_acesso, name="pagina_de_acesso"),
    path("validar_senha/", views.validacao_de_senha, name="validar_senha"),
    path('posts/<int:categoria>', views.posts, name="posts"),
    path('deslogar/', views.deslogar, name="deslogar"),
    path('detalhes/<int:id>/', views.detalhes, name="detalhes"),
    path("deletar/<int:id>", views.apagar_postagem, name="deletar"),
    path("perfil/", views.perfil, name="perfil"),
    path("fazer_postagem/", views.fazer_postagem, name="fazer_postagem"),
    path("salvar_postagem/<int:id>", views.salvar_postagem, name="salvar_postagem"),
    path("editar_postagem/<int:id>", views.editar_postagem, name="editar_postagem"),
    path("opcoes/", views.opcoes, name="opcoes"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)